from __future__ import annotations

import hashlib
import hmac
import os
import re
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DEFAULT_PLAYER_KIT_WIRE = bytes().join(
    (0).to_bytes(4, "little", signed=True)
    + (1).to_bytes(4, "little", signed=True)
    for _ in range(9)
)
DEFAULT_CHARSTATS_WIRE = b"\x00" * 24
DEFAULT_CHARACTER_SLOTS = 3
DEFAULT_CHARACTER_DELETE_SECONDS = 7 * 24 * 60 * 60


class StorageError(RuntimeError):
    pass


class InvalidCredentials(StorageError):
    pass


class InvalidAccountName(StorageError):
    pass


class CharacterNameTaken(StorageError):
    pass


class NoFreeCharacterSlots(StorageError):
    pass


class CharacterNotFound(StorageError):
    pass


@dataclass(frozen=True)
class MariaDBConfig:
    host: str = "127.0.0.1"
    port: int = 3307
    user: str = "root"
    password: str = ""
    database: str = "soemu"


@dataclass(frozen=True)
class AccountRecord:
    id: int
    username: str
    created: bool = False


@dataclass(frozen=True)
class CharacterRecord:
    id: int
    account_id: int
    name: str
    models_wire: bytes
    player_kit_wire: bytes
    is_tutorial_passed: int
    charstats_wire: bytes
    gold_credit: int
    renames_available: int
    rename_required: bool
    deletion_deadline: float | None
    last_space: str
    position: tuple[float, float, float]
    direction: tuple[float, float, float]

    @property
    def deletion_remaining_time(self) -> float:
        if self.deletion_deadline is None:
            return 0.0
        return max(0.0, self.deletion_deadline - time.time())


def normalize_identity(value: str) -> str:
    return unicodedata.normalize("NFKC", value).strip().casefold()


def _password_hash(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=1 << 14,
        r=8,
        p=1,
        dklen=32,
    )


def _new_password_record(password: str) -> tuple[bytes, bytes]:
    salt = os.urandom(16)
    return salt, _password_hash(password, salt)


def _verify_password(password: str, salt: bytes, expected: bytes) -> bool:
    return hmac.compare_digest(_password_hash(password, salt), expected)


class MariaDBRepository:
    """Small synchronous repository for SOEmu's current single process."""

    def __init__(self, config: MariaDBConfig):
        if not re.fullmatch(r"[A-Za-z0-9_]+", config.database):
            raise StorageError("MariaDB database name may contain only A-Z, 0-9 and _")
        self.config = config
        self._driver: Any = None

    def _load_driver(self):
        if self._driver is None:
            try:
                import pymysql
            except ImportError as exc:
                raise StorageError(
                    "Missing PyMySQL. Run: python -m pip install -r requirements.txt"
                ) from exc
            self._driver = pymysql
        return self._driver

    def _connect(self, with_database: bool = True):
        driver = self._load_driver()
        kwargs = dict(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            charset="utf8mb4",
            autocommit=False,
            connect_timeout=5,
            read_timeout=5,
            write_timeout=5,
            cursorclass=driver.cursors.DictCursor,
        )
        if with_database:
            kwargs["database"] = self.config.database
        return driver.connect(**kwargs)

    def initialise(self) -> None:
        with self._connect(with_database=False) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{self.config.database}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            connection.commit()

        statements = [
            statement.strip()
            for statement in SCHEMA_PATH.read_text(encoding="utf-8").split(";")
            if statement.strip()
        ]
        with self._connect() as connection:
            with connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement)
            connection.commit()

    def authenticate_or_create(self, username: str, password: str) -> AccountRecord:
        username = unicodedata.normalize("NFKC", username).strip()
        username_key = normalize_identity(username)
        if not username_key or len(username) > 100:
            raise InvalidAccountName("Account name must contain 1-100 characters")
        if not password:
            raise InvalidCredentials("Password must not be empty")

        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, password_salt, password_hash "
                    "FROM accounts WHERE username_key=%s FOR UPDATE",
                    (username_key,),
                )
                row = cursor.fetchone()
                if row is not None:
                    if not _verify_password(
                        password,
                        bytes(row["password_salt"]),
                        bytes(row["password_hash"]),
                    ):
                        raise InvalidCredentials("Invalid account password")
                    cursor.execute(
                        "UPDATE accounts SET last_login_at=UTC_TIMESTAMP() WHERE id=%s",
                        (row["id"],),
                    )
                    connection.commit()
                    return AccountRecord(int(row["id"]), str(row["username"]), False)

                salt, password_hash = _new_password_record(password)
                cursor.execute(
                    "INSERT INTO accounts "
                    "(username, username_key, password_salt, password_hash, last_login_at) "
                    "VALUES (%s, %s, %s, %s, UTC_TIMESTAMP())",
                    (username, username_key, salt, password_hash),
                )
                account_id = int(cursor.lastrowid)
                connection.commit()
                return AccountRecord(account_id, username, True)

    def is_character_name_available(self, name: str) -> bool:
        name_key = normalize_identity(name)
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM characters WHERE name_key=%s LIMIT 1",
                    (name_key,),
                )
                return cursor.fetchone() is None

    def create_character(
        self,
        account_id: int,
        name: str,
        models_wire: bytes,
    ) -> CharacterRecord:
        if len(models_wire) != 60:
            raise StorageError(
                f"PACKED_AVATAR_MODEL must be 60 bytes, got {len(models_wire)}"
            )
        name = unicodedata.normalize("NFKC", name).strip()
        name_key = normalize_identity(name)
        driver = self._load_driver()

        try:
            with self._connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM accounts WHERE id=%s FOR UPDATE",
                        (account_id,),
                    )
                    if cursor.fetchone() is None:
                        raise StorageError(f"Account {account_id} does not exist")
                    cursor.execute(
                        "SELECT COUNT(*) AS character_count FROM characters "
                        "WHERE account_id=%s",
                        (account_id,),
                    )
                    if int(cursor.fetchone()["character_count"]) >= DEFAULT_CHARACTER_SLOTS:
                        raise NoFreeCharacterSlots("No free character slots")
                    cursor.execute(
                        "INSERT INTO characters "
                        "(account_id, name, name_key, models_wire, player_kit_wire, "
                        "charstats_wire, last_space, position_x, position_y, position_z) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            account_id,
                            name,
                            name_key,
                            models_wire,
                            DEFAULT_PLAYER_KIT_WIRE,
                            DEFAULT_CHARSTATS_WIRE,
                            "spaces/so_origins",
                            37.6137123,
                            6.853166,
                            66.95302,
                        ),
                    )
                    character_id = int(cursor.lastrowid)
                connection.commit()
        except driver.err.IntegrityError as exc:
            raise CharacterNameTaken(name) from exc

        character = self.get_character(account_id, name, include_deleted=True)
        if character is None or character.id != character_id:
            raise StorageError("Created character could not be loaded")
        return character

    def list_characters(self, account_id: int) -> list[CharacterRecord]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM characters WHERE account_id=%s "
                    "AND deletion_deadline IS NOT NULL "
                    "AND deletion_deadline <= UTC_TIMESTAMP()",
                    (account_id,),
                )
                cursor.execute(
                    self._character_select_sql()
                    + " WHERE account_id=%s ORDER BY id",
                    (account_id,),
                )
                rows = cursor.fetchall()
            connection.commit()
        return [self._row_to_character(row) for row in rows]

    def get_character(
        self,
        account_id: int,
        name: str,
        include_deleted: bool = False,
    ) -> CharacterRecord | None:
        where = " WHERE account_id=%s AND name_key=%s"
        if not include_deleted:
            where += " AND deletion_deadline IS NULL"
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    self._character_select_sql() + where + " LIMIT 1",
                    (account_id, normalize_identity(name)),
                )
                row = cursor.fetchone()
        return self._row_to_character(row) if row else None

    def delete_character(
        self,
        account_id: int,
        name: str,
        delete_seconds: int = DEFAULT_CHARACTER_DELETE_SECONDS,
    ) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE characters SET deletion_deadline="
                    "TIMESTAMPADD(SECOND, %s, UTC_TIMESTAMP()) "
                    "WHERE account_id=%s AND name_key=%s AND deletion_deadline IS NULL",
                    (delete_seconds, account_id, normalize_identity(name)),
                )
                if cursor.rowcount != 1:
                    raise CharacterNotFound(name)
            connection.commit()

    def restore_character(self, account_id: int, name: str) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE characters SET deletion_deadline=NULL "
                    "WHERE account_id=%s AND name_key=%s "
                    "AND deletion_deadline > UTC_TIMESTAMP()",
                    (account_id, normalize_identity(name)),
                )
                if cursor.rowcount != 1:
                    raise CharacterNotFound(name)
            connection.commit()

    def set_tutorial_and_location(
        self,
        character_id: int,
        is_tutorial_passed: int,
        space: str,
        position: tuple[float, float, float],
    ) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE characters SET is_tutorial_passed=%s, last_space=%s, "
                    "position_x=%s, position_y=%s, position_z=%s "
                    "WHERE id=%s",
                    (
                        1 if is_tutorial_passed else 0,
                        space,
                        *position,
                        character_id,
                    ),
                )
            connection.commit()

    def update_position(
        self,
        character_id: int,
        space: str,
        position: tuple[float, float, float],
    ) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE characters SET last_space=%s, position_x=%s, "
                    "position_y=%s, position_z=%s WHERE id=%s",
                    (space, *position, character_id),
                )
            connection.commit()

    @staticmethod
    def _character_select_sql() -> str:
        return (
            "SELECT id, account_id, name, models_wire, player_kit_wire, "
            "is_tutorial_passed, charstats_wire, gold_credit, renames_available, "
            "rename_required, UNIX_TIMESTAMP(deletion_deadline) AS deletion_deadline, "
            "last_space, position_x, position_y, position_z, "
            "direction_x, direction_y, direction_z FROM characters"
        )

    @staticmethod
    def _row_to_character(row: dict[str, Any]) -> CharacterRecord:
        deadline = row["deletion_deadline"]
        return CharacterRecord(
            id=int(row["id"]),
            account_id=int(row["account_id"]),
            name=str(row["name"]),
            models_wire=bytes(row["models_wire"]),
            player_kit_wire=bytes(row["player_kit_wire"]),
            is_tutorial_passed=int(row["is_tutorial_passed"]),
            charstats_wire=bytes(row["charstats_wire"]),
            gold_credit=int(row["gold_credit"]),
            renames_available=int(row["renames_available"]),
            rename_required=bool(row["rename_required"]),
            deletion_deadline=float(deadline) if deadline is not None else None,
            last_space=str(row["last_space"]),
            position=(
                float(row["position_x"]),
                float(row["position_y"]),
                float(row["position_z"]),
            ),
            direction=(
                float(row["direction_x"]),
                float(row["direction_y"]),
                float(row["direction_z"]),
            ),
        )
