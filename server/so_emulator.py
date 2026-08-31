#!/usr/bin/env python3
from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import re
import select
import socket
import struct
import time
from dataclasses import dataclass
from pathlib import Path
from avatar_entity_defs import AvatarEntityDefinition

from storage import (
    CharacterNameTaken,
    CharacterNotFound,
    CharacterRecord,
    InvalidAccountName,
    InvalidCredentials,
    MariaDBConfig,
    MariaDBRepository,
    NoFreeCharacterSlots,
    is_valid_world_position,
)

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, modes
    try:
        # Newer cryptography versions move Blowfish here.
        from cryptography.hazmat.decrepit.ciphers.algorithms import Blowfish
    except Exception:
        from cryptography.hazmat.primitives.ciphers.algorithms import Blowfish
except Exception as exc:  # pragma: no cover - friendly Windows runtime message
    raise SystemExit(
        "Stage 18 needs the Python package 'cryptography'.\n"
        "Run: python -m pip install cryptography\n"
        f"Import error: {exc}"
    )

FLAG_HAS_REQUESTS = 0x0001
FLAG_HAS_PIGGYBACKS = 0x0002
FLAG_HAS_ACKS = 0x0004
FLAG_ON_CHANNEL = 0x0008
FLAG_IS_RELIABLE = 0x0010
FLAG_IS_FRAGMENT = 0x0020
FLAG_HAS_SEQUENCE_NUMBER = 0x0040
FLAG_INDEXED_CHANNEL = 0x0080
FLAG_HAS_CHECKSUM = 0x0100
FLAG_CREATE_CHANNEL = 0x0200
FLAG_HAS_CUMULATIVE_ACK = 0x0400
KNOWN_FLAGS = 0x07FF

LOGIN_MESSAGE_ID = 0
LOGIN_VERSION = 58
REPLY_MESSAGE_ID = 0xFF
LOGGED_ON = 1
LOGIN_MALFORMED_REQUEST = 64
LOGIN_BAD_PROTOCOL_VERSION = 65
LOGIN_REJECTED_INVALID_PASSWORD = 67
LOGIN_REJECTED_DB_GENERAL_FAILURE = 70
LOGIN_REJECTED_ILLEGAL_CHARACTERS = 72

ACCOUNT_RESPONSE_EVERYTHING_OK = 0
ACCOUNT_RESPONSE_NO_SUCH_CHARACTER = 1
ACCOUNT_RESPONSE_NOT_ALLOWED_SYMBOLS = 3
ACCOUNT_RESPONSE_TOO_SHORT = 4
ACCOUNT_RESPONSE_TOO_LONG = 5
ACCOUNT_RESPONSE_ALREADY_TAKEN = 6
ACCOUNT_RESPONSE_BEGIN_WITH_GROUND = 7
ACCOUNT_RESPONSE_END_WITH_GROUND = 8
ACCOUNT_RESPONSE_TOO_MANY_GROUNDS = 9
ACCOUNT_RESPONSE_NO_FREE_SLOTS = 11

ENCRYPTION_MAGIC = 0xDEADBEEF
BLOWFISH_BLOCK = 8

# Stage 17/19: real server-owned gameplay spaces.
PLAYER_WORLD_SPACE_ID = 1
PLAYER_WORLD_STATION_GEOMETRY = b"spaces/so_origins"
PLAYER_WORLD_LUBECH_GEOMETRY = b"spaces/city_lubech"
# Saved WorldEditor startPosition values from each space.localsettings.  These
# are known ground-level entry points, unlike the old compatibility (0, 0, 0).
PLAYER_WORLD_STATION_POSITION = (37.6137123, 6.853166, 66.95302)
PLAYER_WORLD_LUBECH_POSITION = (134.237961, 3.75981, 39.83791)
CLIENT_MSG_SPACE_DATA = 0x07
SPACE_DATA_MAPPING_KEY_CLIENT_SERVER = 1
PROPERTY_CHANGE_SINGLE_ID = 61
ENTITY_PROPERTY_FLAG = 0x40
PLAYER_PROPERTY_MESSAGE_ID = (
    0x80 | ENTITY_PROPERTY_FLAG | PROPERTY_CHANGE_SINGLE_ID
)
PLAYER_PASS_TUTORIAL_MESSAGE_ID = PLAYER_PROPERTY_MESSAGE_ID

# Stage 18: Avatar.base.ping() / Avatar.client.pong() from the shipped
# entity_defs. Avatar has 49 exposed base methods, so ping's ordinal 39 is a
# direct top-level index: 0xC0 | 39 == 0xE7. Avatar has 162 client methods;
# BigWorld's subslot rule therefore maps pong ordinal 140 to top index 61 and
# sub-index 79: 0x80 | 61 == 0xBD, followed by sub-index 0x4F in the body.
PLAYER_BASE_PING_EXPOSED_INDEX = 39
PLAYER_BASE_PING_MESSAGE_ID = 0xC0 | PLAYER_BASE_PING_EXPOSED_INDEX
PLAYER_CLIENT_PONG_ORDINAL = 140
PLAYER_CLIENT_PONG_TOP_INDEX = 61
PLAYER_CLIENT_PONG_SUB_INDEX = 79
PLAYER_CLIENT_PONG_MESSAGE_ID = 0x80 | PLAYER_CLIENT_PONG_TOP_INDEX

# BaseAppExtInterface::avatarUpdateImplicit is Coord (3 FLOAT32),
# YawPitchRoll (3 UINT8), and refNum (UINT8).
AVATAR_UPDATE_IMPLICIT_MESSAGE_ID = 2
AVATAR_UPDATE_IMPLICIT_BODY_LENGTH = 16

FLAG_NAMES = [
    (FLAG_HAS_REQUESTS, "HAS_REQUESTS"),
    (FLAG_HAS_PIGGYBACKS, "HAS_PIGGYBACKS"),
    (FLAG_HAS_ACKS, "HAS_ACKS"),
    (FLAG_ON_CHANNEL, "ON_CHANNEL"),
    (FLAG_IS_RELIABLE, "IS_RELIABLE"),
    (FLAG_IS_FRAGMENT, "IS_FRAGMENT"),
    (FLAG_HAS_SEQUENCE_NUMBER, "HAS_SEQUENCE_NUMBER"),
    (FLAG_INDEXED_CHANNEL, "INDEXED_CHANNEL"),
    (FLAG_HAS_CHECKSUM, "HAS_CHECKSUM"),
    (FLAG_CREATE_CHANNEL, "CREATE_CHANNEL"),
    (FLAG_HAS_CUMULATIVE_ACK, "HAS_CUMULATIVE_ACK"),
]

ROOT = Path(__file__).resolve().parent
DEFAULT_RSA_JSON = ROOT / "keys" / "loginapp_private.json"
LOG_PATH = ROOT / "so_emulator.log"


ENTITY_DEFS_ROOT = (
    ROOT.parent
    / "packs"
    / "res"
    / "scripts"
    / "entity_defs"
)

AVATAR_ENTITY_DEF = AvatarEntityDefinition(ENTITY_DEFS_ROOT)

PLAYER_CLIENT_SERVER_PROPERTY_COUNT = (
    AVATAR_ENTITY_DEF.client_property_count
)

PLAYER_PASS_TUTORIAL_PROPERTY_INDEX = (
    AVATAR_ENTITY_DEF.client_property_index("passTutorial")
)

PLAYER_DEFAULT_MODELS_PROPERTY_INDEX = (
    AVATAR_ENTITY_DEF.client_property_index("defaultModels")
)

PLAYER_NAME_PROPERTY_INDEX = (
    AVATAR_ENTITY_DEF.client_property_index("name")
)


SAFE_DEFAULT_MODELS_WIRE = struct.pack(
    "<15i",
    0, 0, 18,
    0, 0, 200006,
    0, 0, 110258,
    0, 0, 110248,
    0, 0, 110253,
)


def normalise_avatar_models_wire(models: bytes) -> bytes:
    if len(models) == 60:
        values = struct.unpack("<15i", models)
        type_ids = (
            values[2],
            values[5],
            values[8],
            values[11],
            values[14],
        )

        if all(type_id > 0 for type_id in type_ids):
            return models

        log(
            "STAGE 20: rejecting invalid defaultModels "
            f"type_ids={type_ids!r}; using safe fallback"
        )
    else:
        log(
            "STAGE 20: rejecting invalid defaultModels "
            f"length={len(models)}; using safe fallback"
        )

    return SAFE_DEFAULT_MODELS_WIRE


def log(msg: str = "") -> None:
    print(msg, flush=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")


def _is_udp_peer_reset(exc: OSError) -> bool:
    """Return whether Windows reported an ICMP port-unreachable peer reset."""
    return isinstance(exc, ConnectionResetError) or getattr(exc, "winerror", None) == 10054


def safe_udp_sendto(sock: socket.socket, data: bytes,
                    addr: tuple[str, int], context: str) -> bool:
    """Send a UDP datagram without letting a departed peer stop SOEmu."""
    try:
        sock.sendto(data, addr)
    except OSError as exc:
        if _is_udp_peer_reset(exc):
            log(f"UDP peer reset (WinError 10054) during {context}, continuing")
            return False
        raise
    return True


def hex_dump(data: bytes, width: int = 16) -> str:
    rows = []
    for off in range(0, len(data), width):
        chunk = data[off:off + width]
        hx = " ".join(f"{b:02x}" for b in chunk)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        rows.append(f"{off:04x}  {hx:<{width*3}}  {asc}")
    return "\n".join(rows)


def flag_text(flags: int) -> str:
    names = [name for bit, name in FLAG_NAMES if flags & bit]
    unknown = flags & ~KNOWN_FLAGS
    if unknown:
        names.append(f"UNKNOWN=0x{unknown:04x}")
    return "|".join(names) if names else "0"


@dataclass
class LoginRequest:
    flags: int
    message_id: int
    body_length: int
    reply_id: int
    next_request_offset: int
    first_request_offset: int
    login_version: int
    rsa_payload: bytes


@dataclass
class LogOnParams:
    flags: int
    username: str
    password: str
    encryption_key: bytes
    digest: bytes
    nonce: int
    trailing: bytes


@dataclass(frozen=True)
class PlayerWorld:
    geometry: bytes
    position: tuple[float, float, float]
    pass_tutorial: int


def select_player_world(world_mode: str, tutorial: int) -> PlayerWorld:
    """Choose the initial world from beginPlay's tutorial flag.

    The client sends 0 when the player chose the tutorial and 1 when it was
    passed/skipped. Explicit station/lubech modes are recovery overrides.
    """
    if world_mode not in {"auto", "station", "lubech"}:
        raise ValueError(f"unknown world mode {world_mode!r}")

    use_station = (
        world_mode == "station"
        or (world_mode == "auto" and tutorial == 0)
    )
    if use_station:
        return PlayerWorld(
            PLAYER_WORLD_STATION_GEOMETRY,
            PLAYER_WORLD_STATION_POSITION,
            0,
        )
    return PlayerWorld(
        PLAYER_WORLD_LUBECH_GEOMETRY,
        PLAYER_WORLD_LUBECH_POSITION,
        1,
    )


def configure_player_world(session: "Session", tutorial: int) -> None:
    world = select_player_world(session.world_mode, tutorial)
    session.play_geometry = world.geometry
    session.play_position = world.position
    session.play_pass_tutorial = world.pass_tutorial


def configure_player_character(
    session: "Session",
    character: CharacterRecord,
    tutorial: int,
) -> None:
    """Apply beginPlay choice and reject corrupted persisted coordinates."""
    if session.world_mode != "auto":
        configure_player_world(session, tutorial)
        return

    requested_world = select_player_world("auto", tutorial)

    persisted_geometry = character.last_space.encode(
        "ascii",
        "ignore",
    )

    supported = {
        PLAYER_WORLD_STATION_GEOMETRY,
        PLAYER_WORLD_LUBECH_GEOMETRY,
    }

    persisted_position_valid = is_valid_world_position(
        character.position
    )

    if not persisted_position_valid:
        log(
            "STAGE 20: corrupted persisted position rejected: "
            f"character_id={character.id}, "
            f"position={character.position!r}"
        )

    may_resume = (
        persisted_geometry in supported
        and persisted_position_valid
        and (
            persisted_geometry == requested_world.geometry
            or (
                tutorial != 0
                and character.is_tutorial_passed != 0
            )
        )
    )

    if may_resume:
        session.play_geometry = persisted_geometry
        session.play_position = character.position
    else:
        session.play_geometry = requested_world.geometry
        session.play_position = requested_world.position

    session.play_pass_tutorial = (
        0 if tutorial == 0 else 1
    )

    if not is_valid_world_position(session.play_position):
        raise RuntimeError(
            "STAGE 20 selected an invalid player spawn: "
            f"{session.play_position!r}"
        )


@dataclass
class Session:
    username: str
    account_id: int
    blowfish_key: bytes
    login_session_key: int
    login_client_addr: tuple[str, int]
    created_at: float
    base_client_addr: tuple[str, int] | None = None
    server_session_key: int = 0
    base_logged_in: bool = False
    post_login_packets: int = 0

    # Mercury channel state. SOnline uses the standard 28-bit BigWorld
    # sequence space, but this stage only needs normal non-wraparound startup.
    client_next_expected_seq: int = 0

    # Mercury keeps reliable and non-reliable packet sequence sources
    # separately on this client.  The Stage 8 trace proves it: after client
    # reliable seq=0, ACK-only packets used seq=1/2/3, then disconnectClient
    # arrived as reliable seq=1 again.
    server_reliable_seq: int = 0
    server_unreliable_seq: int = 0

    last_server_send: float = 0.0
    server_auth_sent: bool = False
    client_init_sent: bool = False
    client_init_acked: bool = False
    channel_started: bool = False
    enable_entities_seen: bool = False

    # Stage 10: create Account only after the client has ACKed a separate
    # updateFrequency/tickSync/setGameTime initialization packet.
    account_create_sent: bool = False
    account_create_due: float = 0.0
    account_entity_id: int = 1

    # Stage 10: Account.base.requestCharacterList() ->
    # Account.client.receiveCharacterList([]).
    request_character_list_seen: bool = False
    character_list_sent: bool = False
    character_list_acked: bool = False
    character_list_due: float = 0.0
    character_list_seq: int = -1

    # Stage 15: AvatarDummy must exist BEFORE receiveCharacterList([]) opens
    # the Character Picker. Stage 13 proved that creating it afterwards leaves
    # DummyRotating without .angle and the 3D preview blank.
    avatar_dummy_entity_id: int = 2
    avatar_dummy_type_id: int = 10
    avatar_enter_due: float = 0.0
    avatar_enter_sent: bool = False
    avatar_enter_acked: bool = False
    avatar_enter_seq: int = -1
    avatar_create_due: float = 0.0
    avatar_detailed_sent: bool = False
    avatar_detailed_acked: bool = False
    avatar_detailed_seq: int = -1

    create_avatar_seen: bool = False
    created_avatar_name: str = ""
    created_default_models_wire: bytes = b""
    create_callback_sent: bool = False
    create_callback_succeeded: bool = False
    create_callback_acked: bool = False
    create_callback_seq: int = -1
    created_character_list_due: float = 0.0
    created_character_list_sent: bool = False
    created_character_list_seq: int = -1

    # Stage 15: Account.base.beginPlay -> PlayerAvatar base/cell player.
    begin_play_seen: bool = False
    begin_play_name: str = ""
    begin_play_tutorial: int = 0
    player_avatar_entity_id: int = 3
    player_avatar_type_id: int = 1
    # Stage 17: PlayerAvatar enters a normal server-owned space.
    # 0x40000000 remains reserved for the client-local personages_select space.
    play_space_id: int = PLAYER_WORLD_SPACE_ID
    world_mode: str = "auto"
    play_geometry: bytes = PLAYER_WORLD_LUBECH_GEOMETRY
    play_position: tuple[float, float, float] = PLAYER_WORLD_LUBECH_POSITION
    play_pass_tutorial: int = 1
    active_character_id: int = 0
    active_default_models_wire: bytes = b""
    position_dirty: bool = False
    last_position_save: float = 0.0
    player_base_sent: bool = False
    player_base_acked: bool = False
    player_base_seq: int = -1
    player_cell_due: float = 0.0
    player_cell_sent: bool = False
    player_cell_acked: bool = False
    player_cell_seq: int = -1
    player_tutorial_property_sent: bool = False
    player_tutorial_property_acked: bool = False
    player_tutorial_property_seq: int = -1
    player_space_data_sent: bool = False
    player_space_data_acked: bool = False
    player_space_data_seq: int = -1


@dataclass
class BaseAppLoginRequest:
    flags: int
    message_id: int
    body_length: int
    reply_id: int
    next_request_offset: int
    first_request_offset: int
    login_key: int
    attempt: int



def parse_baseapp_login_request(data: bytes) -> BaseAppLoginRequest:
    """Parse the real plaintext SOnline baseAppLogin request observed on 0.6.5.3."""
    if len(data) < 21:
        raise ValueError("BaseApp datagram is too short")

    flags = struct.unpack_from("<H", data, 0)[0]
    if not (flags & FLAG_HAS_REQUESTS):
        raise ValueError(f"expected HAS_REQUESTS, got flags=0x{flags:04x}")

    # For HAS_REQUESTS the last uint16 is the first request offset.
    first_request_offset = struct.unpack_from("<H", data, len(data) - 2)[0]
    message_end = len(data) - 2
    off = first_request_offset

    if off < 2 or off + 9 > message_end:
        raise ValueError(f"invalid first request offset {off}")

    message_id = data[off]
    body_length = struct.unpack_from("<H", data, off + 1)[0]
    reply_id = struct.unpack_from("<i", data, off + 3)[0]
    next_request_offset = struct.unpack_from("<H", data, off + 7)[0]

    body_off = off + 9
    body_end = body_off + body_length
    if body_end > message_end:
        raise ValueError(
            f"BaseApp body overruns datagram: body_end={body_end}, message_end={message_end}"
        )

    # baseAppLogin is the first BaseAppExtInterface message and its body is:
    # SessionKey (uint32) + attempt (int32) = 8 bytes.
    if message_id != 0:
        raise ValueError(f"not baseAppLogin: message_id={message_id}")
    if body_length != 8:
        raise ValueError(f"unexpected baseAppLogin body length {body_length}")

    login_key, attempt = struct.unpack_from("<II", data, body_off)

    return BaseAppLoginRequest(
        flags=flags,
        message_id=message_id,
        body_length=body_length,
        reply_id=reply_id,
        next_request_offset=next_request_offset,
        first_request_offset=first_request_offset,
        login_key=login_key,
        attempt=attempt,
    )


@dataclass
class ChannelPacket:
    flags: int
    sequence: int | None
    cumulative_ack: int | None
    acks: list[int]
    message_bytes: bytes


def parse_channel_packet(plain: bytes) -> ChannelPacket:
    """Strip the Mercury channel footers seen in the real SOnline client."""
    if len(plain) < 2:
        raise ValueError("channel packet shorter than flags")

    flags = struct.unpack_from("<H", plain, 0)[0]
    if flags & ~KNOWN_FLAGS:
        raise ValueError(f"unknown Mercury flags 0x{flags:04x}")

    end = len(plain)
    cumulative_ack = None
    acks: list[int] = []
    sequence = None

    # BigWorld PacketReceiver strips these in this order:
    # cumulative ACK -> ACK count/ACKs -> sequence number.
    if flags & FLAG_HAS_CUMULATIVE_ACK:
        if end - 4 < 2:
            raise ValueError("missing cumulative ACK footer")
        end -= 4
        cumulative_ack = struct.unpack_from("<I", plain, end)[0]

    if flags & FLAG_HAS_ACKS:
        if end - 1 < 2:
            raise ValueError("missing ACK count footer")
        end -= 1
        ack_count = plain[end]
        if ack_count == 0:
            raise ValueError("HAS_ACKS with zero ACK count")
        need = ack_count * 4
        if end - need < 2:
            raise ValueError("ACK footer overruns packet")
        # packFooter writes ACKs backwards; order is not important for us.
        for _ in range(ack_count):
            end -= 4
            acks.append(struct.unpack_from("<I", plain, end)[0])

    if flags & FLAG_HAS_SEQUENCE_NUMBER:
        if end - 4 < 2:
            raise ValueError("missing sequence footer")
        end -= 4
        sequence = struct.unpack_from("<I", plain, end)[0]

    return ChannelPacket(
        flags=flags,
        sequence=sequence,
        cumulative_ack=cumulative_ack,
        acks=acks,
        message_bytes=plain[2:end],
    )


def describe_baseapp_messages(session: Session, message_bytes: bytes) -> dict[str, bool]:
    """Decode BaseApp startup, movement, and exposed entity RPC traffic."""
    pos = 0
    found = {
        "authenticate": False,
        "enableEntities": False,
        "disconnectClient": False,
        "requestCharacterList": False,
        "requestEntityUpdate": False,
        "nameCheckUid": None,
        "createAvatarName": None,
        "createAvatarBody": None,
        "deleteAvatarName": None,
        "restoreCharacterName": None,
        "beginPlayName": None,
        "beginPlayTutorial": None,
        "playerPing": False,
    }

    # Confirmed Account BASE exposed-method mapping for this client build.
    # BigWorld client startProxyMessage() sends 0xC0 | exposedIndex.
    account_base_rpc_names = {
        0xC7: "restoreCharacter",                  # exposed index 7
        0xC9: "playerCheckAvatarNameAvailability",  # exposed index 9
        0xCA: "requestCharacterList",              # exposed index 10
        0xCB: "createNewAvatar",                   # exposed index 11
        0xCC: "deleteAvatar",                      # exposed index 12
        0xCD: "beginPlay",                         # exposed index 13
    }

    while pos < len(message_bytes):
        msg_id = message_bytes[pos]
        pos += 1

        # BaseAppExtInterface IDs in BigWorld 2.x:
        #   0 baseAppLogin (off-channel variable request)
        #   1 authenticate(SessionKey)
        #  10 enableEntities(uint8)
        #  12 disconnectClient(uint8)
        if msg_id == 1:
            if pos + 4 > len(message_bytes):
                log("  MSG authenticate: TRUNCATED")
                break
            key = struct.unpack_from("<I", message_bytes, pos)[0]
            pos += 4
            found["authenticate"] = True
            match = key == session.server_session_key
            log(f"  MSG 01 authenticate : key=0x{key:08x} "
                f"({'MATCH' if match else 'MISMATCH'})")

        elif msg_id == AVATAR_UPDATE_IMPLICIT_MESSAGE_ID:
            if pos + AVATAR_UPDATE_IMPLICIT_BODY_LENGTH > len(message_bytes):
                log("  MSG 02 avatarUpdateImplicit: TRUNCATED")
                break

            body = message_bytes[
                pos:pos + AVATAR_UPDATE_IMPLICIT_BODY_LENGTH
            ]
            pos += AVATAR_UPDATE_IMPLICIT_BODY_LENGTH

            x, y, z = struct.unpack_from(">fff", body, 0)
            yaw, pitch, roll, ref_num = struct.unpack_from(
                "<BBBB",
                body,
                12,
            )

            candidate_position = (x, y, z)

            if session.active_character_id:
                if is_valid_world_position(candidate_position):
                    session.play_position = candidate_position
                    session.position_dirty = True
                else:
                    log(
                        "  MSG 02 avatarUpdateImplicit: "
                        "REJECTED INVALID POSITION "
                        f"{candidate_position!r}"
                    )

            log(
                "  MSG 02 avatarUpdateImplicit: "
                f"pos=({x:g}, {y:g}, {z:g}), "
                f"dir=({yaw}, {pitch}, {roll}), "
                f"refNum={ref_num}"
            )

        elif msg_id == 10:
            if pos >= len(message_bytes):
                log("  MSG 10 enableEntities: TRUNCATED")
                break
            dummy = message_bytes[pos]
            pos += 1
            found["enableEntities"] = True
            session.enable_entities_seen = True
            log(f"  MSG 10 enableEntities: dummy={dummy}")

        elif msg_id == 12:
            if pos >= len(message_bytes):
                log("  MSG 12 disconnectClient: TRUNCATED")
                break
            reason = message_bytes[pos]
            pos += 1
            found["disconnectClient"] = True
            log(f"  MSG 12 disconnectClient: reason={reason}")

        elif msg_id == 8:
            log("  MSG 08 switchInterface")

        elif msg_id == 9:
            if pos + 2 > len(message_bytes):
                log("  MSG 09 requestEntityUpdate: TRUNCATED LENGTH")
                break
            ln = struct.unpack_from("<H", message_bytes, pos)[0]
            pos += 2
            if pos + ln > len(message_bytes):
                log(f"  MSG 09 requestEntityUpdate: TRUNCATED BODY ({ln})")
                break
            body = message_bytes[pos:pos + ln]
            pos += ln
            found["requestEntityUpdate"] = True
            log(f"  MSG 09 requestEntityUpdate: {ln} bytes / {body.hex()}")
            if len(body) >= 4:
                requested_id = struct.unpack_from("<i", body, 0)[0]
                log(f"    requested EntityID: {requested_id}")

        elif msg_id >= 128:
            # BaseAppExtInterface::entityMessage is variable length (uint16).
            if pos + 2 > len(message_bytes):
                log(f"  MSG {msg_id:02x} entityMessage: TRUNCATED LENGTH")
                break
            ln = struct.unpack_from("<H", message_bytes, pos)[0]
            pos += 2
            if pos + ln > len(message_bytes):
                log(f"  MSG {msg_id:02x} entityMessage: TRUNCATED BODY ({ln})")
                break
            body = message_bytes[pos:pos + ln]
            pos += ln

            rpc_name = account_base_rpc_names.get(msg_id)
            if rpc_name:
                log(
                    f"  MSG {msg_id:02x} Account.base.{rpc_name}: "
                    f"{ln} bytes / {body.hex()}"
                )
            else:
                log(f"  MSG {msg_id:02x} entityMessage: {ln} bytes / {body.hex()}")

            if (
                msg_id == PLAYER_BASE_PING_MESSAGE_ID
                and ln == 0
                and session.player_base_sent
            ):
                found["playerPing"] = True
                log("")
                log(">>> PLAYER PING RECEIVED <<<")
                log("    method             : Avatar.base.ping")
                log(f"    Mercury message ID : 0x{msg_id:02X}")
                log(f"    Exposed index      : {PLAYER_BASE_PING_EXPOSED_INDEX}")
                log("    Arguments          : none")
                log("")

            elif msg_id == 0xCA and ln == 0:
                found["requestCharacterList"] = True
                session.request_character_list_seen = True
                log("")
                log(">>> ACCOUNT RPC CONFIRMED: requestCharacterList() <<<")
                log("    Mercury message ID : 0xCA")
                log("    Base exposed index : 10")
                log("    Arguments          : none")
                log("")
            elif msg_id == 0xC9:
                # Account.base.playerCheckAvatarNameAvailability(UNICODE_STRING).
                # BigWorld UNICODE_STRING is UTF-8 encoded through BinaryOStream::
                # appendString(): 1-byte length for strings < 255, then bytes.
                if body:
                    strlen = body[0]
                    if strlen == 0xFF:
                        if len(body) >= 4:
                            strlen = body[1] | (body[2] << 8) | (body[3] << 16)
                            str_off = 4
                        else:
                            strlen = -1
                            str_off = len(body)
                    else:
                        str_off = 1
                    if strlen >= 0 and str_off + strlen <= len(body):
                        raw_uid = body[str_off:str_off + strlen]
                        try:
                            uid = raw_uid.decode("utf-8")
                        except UnicodeDecodeError:
                            uid = raw_uid.decode("utf-8", "replace")
                        found["nameCheckUid"] = uid
                        log("")
                        log(">>> NAME CHECK RPC CONFIRMED <<<")
                        log(f"    uid                 : {uid!r}")
                        log(f"    raw                 : {body.hex()}")
                        log("")
            elif msg_id == 0xCB:
                found["createAvatarBody"] = body
                if body:
                    strlen = body[0]
                    if strlen == 0xFF:
                        if len(body) >= 4:
                            strlen = body[1] | (body[2] << 8) | (body[3] << 16)
                            str_off = 4
                        else:
                            strlen = -1
                            str_off = len(body)
                    else:
                        str_off = 1
                    if strlen >= 0 and str_off + strlen <= len(body):
                        raw_name = body[str_off:str_off + strlen]
                        try:
                            avatar_name = raw_name.decode("utf-8")
                        except UnicodeDecodeError:
                            avatar_name = raw_name.decode("utf-8", "replace")
                        found["createAvatarName"] = avatar_name
                        session.create_avatar_seen = True
                        session.created_avatar_name = avatar_name
                        # createNewAvatar has exactly two args in Account.def:
                        # UNICODE_STRING name + PACKED_AVATAR_MODEL.  Preserve
                        # the fixed-dict bytes byte-for-byte so the follow-up
                        # CHARACTER_INFO uses the exact model choices supplied
                        # by the real client UI.
                        models_wire = body[str_off + strlen:]
                        session.created_default_models_wire = models_wire
                        log("")
                        log(">>> CREATE NEW AVATAR RPC CONFIRMED <<<")
                        log(f"    avatar_name          : {avatar_name!r}")
                        log(f"    defaultModels bytes  : {len(models_wire)}")
                        log(f"    full body            : {body.hex()}")
                        log("")

            elif msg_id in (0xC7, 0xCC):
                try:
                    raw_name, end = read_packed_string(body, 0)
                    if end != len(body):
                        raise ValueError(f"{len(body) - end} trailing bytes")
                    character_name = raw_name.decode("utf-8")
                except (ValueError, UnicodeDecodeError) as exc:
                    log(f"    invalid character name argument: {exc}")
                else:
                    key = (
                        "restoreCharacterName" if msg_id == 0xC7
                        else "deleteAvatarName"
                    )
                    found[key] = character_name
                    log(f"    character_name      : {character_name!r}")

            elif msg_id == 0xCD:
                # Account.base.beginPlay(UNICODE_STRING name, INT8 tutorial).
                if body:
                    strlen = body[0]
                    if strlen == 0xFF:
                        if len(body) >= 4:
                            strlen = body[1] | (body[2] << 8) | (body[3] << 16)
                            str_off = 4
                        else:
                            strlen = -1
                            str_off = len(body)
                    else:
                        str_off = 1
                    if strlen >= 0 and str_off + strlen + 1 <= len(body):
                        raw_name = body[str_off:str_off + strlen]
                        try:
                            play_name = raw_name.decode("utf-8")
                        except UnicodeDecodeError:
                            play_name = raw_name.decode("utf-8", "replace")
                        tutorial = struct.unpack_from("<b", body, str_off + strlen)[0]
                        found["beginPlayName"] = play_name
                        found["beginPlayTutorial"] = tutorial
                        session.begin_play_seen = True
                        session.begin_play_name = play_name
                        session.begin_play_tutorial = tutorial
                        log("")
                        log(">>> BEGIN PLAY RPC CONFIRMED <<<")
                        log(f"    avatar_name          : {play_name!r}")
                        log(f"    tutorial             : {tutorial}")
                        log(f"    raw                  : {body.hex()}")
                        log("")

            elif session.account_create_sent:
                log("")
                log(">>> NEXT ACCOUNT RPC CAPTURED <<<")
                log(f"    Mercury entity msg id : 0x{msg_id:02x} ({msg_id})")
                if rpc_name:
                    log(f"    Known method          : Account.base.{rpc_name}()")
                log(f"    Body length           : {ln}")
                log(f"    Body hex              : {body.hex()}")
                log("")

        else:
            remaining = message_bytes[pos:]
            log(f"  MSG {msg_id:02x}: not decoded by Stage 18; "
                f"remaining={remaining.hex()}")
            break

    return found


def build_server_channel_packet(session: Session, message_bytes: bytes = b"",
                                reliable: bool = False) -> tuple[bytes, bytes, int]:
    """Build one addressed external Mercury channel packet for SOnline."""
    flags = FLAG_ON_CHANNEL | FLAG_HAS_SEQUENCE_NUMBER | FLAG_HAS_CUMULATIVE_ACK

    if reliable:
        flags |= FLAG_IS_RELIABLE
        seq = session.server_reliable_seq
        session.server_reliable_seq = (
            session.server_reliable_seq + 1
        ) & 0x0FFFFFFF
    else:
        seq = session.server_unreliable_seq
        session.server_unreliable_seq = (
            session.server_unreliable_seq + 1
        ) & 0x0FFFFFFF

    clear = (
        struct.pack("<H", flags)
        + message_bytes
        + struct.pack("<I", seq)
        + struct.pack("<I", session.client_next_expected_seq)
    )
    encrypted = encrypt_filtered_packet(session.blowfish_key, clear)
    return clear, encrypted, seq


def send_channel_ack(base_sock: socket.socket, session: Session,
                     addr: tuple[str, int], reason: str) -> None:
    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=b"", reliable=False
    )
    safe_udp_sendto(base_sock, encrypted, addr, "channel ACK")
    session.last_server_send = time.time()
    log(f"TX CHANNEL ACK : seq={seq}, cumAck={session.client_next_expected_seq}, "
        f"{len(encrypted)} encrypted bytes ({reason})")
    log("ACK clear hex:\n" + hex_dump(clear))


def send_player_pong(base_sock: socket.socket, session: Session,
                     addr: tuple[str, int]) -> None:
    """Send Avatar.client.pong() using BigWorld's client-method subslot."""
    args = bytes([PLAYER_CLIENT_PONG_SUB_INDEX])
    body = struct.pack("<i", session.player_avatar_entity_id) + args
    msg = (
        bytes([PLAYER_CLIENT_PONG_MESSAGE_ID])
        + struct.pack("<H", len(body))
        + body
    )
    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "Avatar.client.pong")
    session.last_server_send = time.time()
    log("TX PLAYER PONG:")
    log(f"    EntityID          = {session.player_avatar_entity_id}")
    log("    method            = Avatar.client.pong")
    log(f"    ordinal           = {PLAYER_CLIENT_PONG_ORDINAL}")
    log(f"    top/sub index      = {PLAYER_CLIENT_PONG_TOP_INDEX}/{PLAYER_CLIENT_PONG_SUB_INDEX}")
    log(f"    msg                = 0x{PLAYER_CLIENT_PONG_MESSAGE_ID:02X}")
    log("    args               = none")
    log(f"    body length        = {len(body)}")
    log(f"    seq                = {seq}")
    log(f"    cumAck             = {session.client_next_expected_seq}")
    log("PLAYER PONG clear hex:\n" + hex_dump(clear))


def send_server_auth(base_sock: socket.socket, session: Session,
                     addr: tuple[str, int]) -> None:
    # ClientInterface::authenticate is message ID 0, fixed uint32 SessionKey.
    msg = bytes([0]) + struct.pack("<I", session.server_session_key)
    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "server authenticate")
    session.server_auth_sent = True
    session.last_server_send = time.time()
    log(f"TX SERVER AUTH : seq={seq}, key=0x{session.server_session_key:08x}, "
        f"cumAck={session.client_next_expected_seq}")
    log("SERVER AUTH clear hex:\n" + hex_dump(clear))




def send_client_init(base_sock: socket.socket, session: Session,
                     addr: tuple[str, int]) -> None:
    """
    BaseApp -> ClientInterface startup state.

    Verified against the SOnline executable / BigWorld layout:
      ID 0x02 updateFrequencyNotification : fixed uint8
      ID 0x0e tickSync                    : fixed uint8
      ID 0x03 setGameTime                 : fixed uint32

    Real BigWorld servers prime the client timing state before player entity
    creation.  Keep this as its own reliable/flushed packet; do not append
    CREATE_BASE_PLAYER to the same datagram.
    """
    hertz = 10
    tick_byte = 0

    # An absolute tick value is enough for startup.  It advances at the same
    # nominal 10 Hz rate advertised above and naturally fits uint32.
    game_time = int(time.monotonic() * hertz) & 0xFFFFFFFF

    msg = (
        bytes([2, hertz]) +
        bytes([14, tick_byte]) +
        bytes([3]) + struct.pack("<I", game_time)
    )

    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "client timing init")
    session.client_init_sent = True
    session.last_server_send = time.time()

    log(
        f"TX CLIENT INIT : reliable seq={seq}, hertz={hertz}, "
        f"tick={tick_byte}, gameTime={game_time}, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("CLIENT INIT clear hex:\n" + hex_dump(clear))
    log(
        ">>> Stage 10 milestone B: updateFrequency + tickSync + setGameTime "
        "sent in a separate reliable packet.\n"
    )



def send_create_base_player(base_sock: socket.socket, session: Session,
                            addr: tuple[str, int]) -> None:
    """
    ClientInterface::createBasePlayer is interface message ID 5 and is
    VARIABLE_LENGTH_MESSAGE with a 2-byte length field.

    ServerConnection::createBasePlayer consumes:
        EntityID      int32
        EntityTypeID  uint16
        remaining stream = base+client properties

    BigWorld EntityType::newDictionary() explicitly uses default property
    values when remainingLength() == 0, so for the first compatibility test
    we intentionally send no Account property payload.

    In this SOnline entities.xml Account is the first client entity type, so
    Account's client EntityTypeID is 0.
    """
    entity_id = session.account_entity_id
    account_type_id = 0

    body = struct.pack("<iH", entity_id, account_type_id)
    msg = bytes([5]) + struct.pack("<H", len(body)) + body

    clear, encrypted, seq = build_server_channel_packet(
        session,
        message_bytes=msg,
        reliable=True,
    )
    safe_udp_sendto(base_sock, encrypted, addr, "create Account base player")
    session.account_create_sent = True
    session.last_server_send = time.time()

    log(
        f"TX CREATE ACCOUNT: reliable seq={seq}, EntityID={entity_id}, "
        f"EntityTypeID={account_type_id}, payload={len(body)} bytes, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("CREATE ACCOUNT clear hex:\n" + hex_dump(clear))
    log(
        ">>> Stage 10 milestone C: ClientInterface::createBasePlayer(Account) sent."
    )
    log(
        ">>> Client should print 'Account onBecomePlayer' and then call "
        "account.base.requestCharacterList().\n"
    )


def send_avatar_base_player(
    base_sock: socket.socket,
    session: Session,
    addr: tuple[str, int],
) -> None:
    """
    Stage 20 PlayerAvatar bootstrap.

    createBasePlayer receives the complete BASE_AND_CLIENT stream.

    Avatar.name and Avatar.defaultModels are ALL_CLIENTS properties,
    therefore BigWorld does not permit them inside BASE_PLAYER_DATA.
    They are emitted immediately after createBasePlayer in the SAME
    reliable Mercury bundle, before createCellPlayer can be scheduled.
    """
    if not session.begin_play_name:
        raise RuntimeError(
            "cannot bootstrap PlayerAvatar without Avatar.name"
        )

    models = normalise_avatar_models_wire(
        session.active_default_models_wire
    )
    session.active_default_models_wire = models

    base_property_stream = (
        AVATAR_ENTITY_DEF.build_base_player_stream()
    )

    if not base_property_stream:
        raise RuntimeError(
            "PlayerAvatar BASE_PLAYER_DATA is empty"
        )

    base_body = (
        struct.pack(
            "<iH",
            session.player_avatar_entity_id,
            session.player_avatar_type_id,
        )
        + base_property_stream
    )

    create_base_message = (
        bytes([5])
        + struct.pack("<H", len(base_body))
        + base_body
    )

    name_message = build_player_top_level_property_message(
        session,
        PLAYER_NAME_PROPERTY_INDEX,
        _pack_bigworld_string(session.begin_play_name),
    )

    models_message = build_player_top_level_property_message(
        session,
        PLAYER_DEFAULT_MODELS_PROPERTY_INDEX,
        models,
    )

    bootstrap_messages = (
        create_base_message
        + name_message
        + models_message
    )

    clear, encrypted, seq = build_server_channel_packet(
        session,
        message_bytes=bootstrap_messages,
        reliable=True,
    )

    safe_udp_sendto(
        base_sock,
        encrypted,
        addr,
        "PlayerAvatar Stage 20 bootstrap",
    )

    session.player_base_sent = True
    session.player_base_seq = seq
    session.last_server_send = time.time()

    log(
        "TX AVATAR BOOTSTRAP: "
        f"reliable seq={seq}, "
        f"EntityID={session.player_avatar_entity_id}, "
        f"EntityTypeID={session.player_avatar_type_id}, "
        f"name={session.begin_play_name!r}, "
        f"BASE_PLAYER_DATA={len(base_property_stream)} bytes, "
        f"BASE properties={len(AVATAR_ENTITY_DEF.base_property_names)}, "
        f"clientProperties={PLAYER_CLIENT_SERVER_PROPERTY_COUNT}, "
        f"nameIndex={PLAYER_NAME_PROPERTY_INDEX}, "
        f"defaultModelsIndex={PLAYER_DEFAULT_MODELS_PROPERTY_INDEX}, "
        f"defaultModelsHeadType="
        f"{struct.unpack_from('<i', models, 8)[0]}, "
        f"cumAck={session.client_next_expected_seq}"
    )

    log(
        "AVATAR BOOTSTRAP clear hex:\n"
        + hex_dump(clear)
    )

    log(
        ">>> Stage 20 milestone A: "
        "createBasePlayer + Avatar.name + Avatar.defaultModels "
        "sent atomically."
    )
    log(
        ">>> PlayerAvatar no longer starts from an empty "
        "base property stream.\n"
    )


def build_avatar_cell_player_message(session: Session) -> bytes:
    """Build ClientInterface::createCellPlayer for the selected start point."""
    body = (
        struct.pack("<ii", session.play_space_id, 0)
        + struct.pack("<fff", *session.play_position)
        + struct.pack("<fff", 0.0, 0.0, 0.0)
    )
    return bytes([6]) + struct.pack("<H", len(body)) + body


def send_avatar_cell_player(base_sock: socket.socket, session: Session,
                            addr: tuple[str, int]) -> None:
    """Enter PlayerAvatar into server-owned SpaceID 1.

    ClientInterface::createCellPlayer (ID 6) payload:
      SpaceID int32, vehicleID int32, Position3D (3 floats),
      Direction3D (3 floats), optional cell/client property stream.

    Geometry is mapped by a separate reliable ClientInterface::spaceData
    message after this createCellPlayer packet is ACKed by the client.
    """
    msg = build_avatar_cell_player_message(session)
    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "create Avatar cell player")
    session.player_cell_sent = True
    session.player_cell_seq = seq
    session.last_server_send = time.time()
    log(
        f"TX AVATAR CELL PLAYER: reliable seq={seq}, "
        f"EntityID(current)={session.player_avatar_entity_id}, "
        f"spaceID={session.play_space_id}, vehicleID=0, "
        f"pos={session.play_position!r}, dir=(0,0,0), "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("AVATAR CELL clear hex:\n" + hex_dump(clear))
    log(">>> Stage 19 milestone B: createCellPlayer(spaceID=1) sent.")
    log(">>> Waiting for its ACK before setting passTutorial.\n")


def pack_high_top_level_property_path(index: int, property_count: int) -> bytes:
    """Encode BigWorld PropertyChange::SINGLE's empty-path top-level index."""
    if property_count <= 1:
        raise ValueError("property_count must be greater than one")
    if not 0 <= index < property_count:
        raise ValueError(f"property index {index} outside count {property_count}")

    index_bits = (property_count - 1).bit_length()
    bits = [0]  # stop: this is the top-level property, with no nested path
    bits.extend((index >> shift) & 1 for shift in range(index_bits - 1, -1, -1))
    while len(bits) % 8:
        bits.append(0)

    result = bytearray(len(bits) // 8)
    for bit_offset, bit in enumerate(bits):
        if bit:
            result[bit_offset // 8] |= 1 << (7 - (bit_offset % 8))
    return bytes(result)
    
    
def build_player_top_level_property_message(
    session: Session,
    property_index: int,
    value_wire: bytes,
) -> bytes:
    if not 0 <= property_index < PLAYER_CLIENT_SERVER_PROPERTY_COUNT:
        raise ValueError(
            f"Avatar client property index {property_index} "
            f"outside count {PLAYER_CLIENT_SERVER_PROPERTY_COUNT}"
        )

    if property_index < PROPERTY_CHANGE_SINGLE_ID:
        msg_id = (
            0x80
            | ENTITY_PROPERTY_FLAG
            | property_index
        )

        body = (
            struct.pack(
                "<i",
                session.player_avatar_entity_id,
            )
            + value_wire
        )
    else:
        msg_id = PLAYER_PROPERTY_MESSAGE_ID

        property_path = pack_high_top_level_property_path(
            property_index,
            PLAYER_CLIENT_SERVER_PROPERTY_COUNT,
        )

        body = (
            struct.pack(
                "<i",
                session.player_avatar_entity_id,
            )
            + property_path
            + value_wire
        )

    return (
        bytes([msg_id])
        + struct.pack("<H", len(body))
        + body
    )


def build_player_pass_tutorial_message(session: Session) -> bytes:
    """Build Avatar.passTutorial's reliable entity-property update."""
    if session.play_pass_tutorial not in (0, 1):
        raise ValueError("passTutorial must be 0 or 1")
    property_path = pack_high_top_level_property_path(
        PLAYER_PASS_TUTORIAL_PROPERTY_INDEX,
        PLAYER_CLIENT_SERVER_PROPERTY_COUNT,
    )
    body = (
        struct.pack("<i", session.player_avatar_entity_id)
        + property_path
        + struct.pack("<b", session.play_pass_tutorial)
    )
    return (
        bytes([PLAYER_PASS_TUTORIAL_MESSAGE_ID])
        + struct.pack("<H", len(body))
        + body
    )


def send_player_pass_tutorial(base_sock: socket.socket, session: Session,
                              addr: tuple[str, int]) -> None:
    msg = build_player_pass_tutorial_message(session)
    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "Avatar.passTutorial property")
    session.player_tutorial_property_sent = True
    session.player_tutorial_property_seq = seq
    session.last_server_send = time.time()
    log(
        f"TX AVATAR passTutorial: reliable seq={seq}, "
        f"msg=0x{PLAYER_PASS_TUTORIAL_MESSAGE_ID:02x}, "
        f"EntityID={session.player_avatar_entity_id}, "
        f"propertyIndex={PLAYER_PASS_TUTORIAL_PROPERTY_INDEX}, "
        f"value={session.play_pass_tutorial}, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("AVATAR passTutorial clear hex:\n" + hex_dump(clear))
    log(">>> Waiting for passTutorial ACK before mapping geometry.\n")


def build_player_space_data_message(session: Session) -> bytes:
    """Build ClientInterface::spaceData for the selected geometry."""
    space_entry_id = struct.pack(
        "<IHH",
        0,  # ip
        0,  # port
        1,  # salt: stable non-zero mapping identifier
    )

    identity_matrix = struct.pack(
        "<16f",
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )

    body = (
        struct.pack("<i", session.play_space_id)
        + space_entry_id
        + struct.pack("<H", SPACE_DATA_MAPPING_KEY_CLIENT_SERVER)
        + identity_matrix
        + session.play_geometry
    )
    expected_length = 78 + len(session.play_geometry)
    if len(body) != expected_length:
        raise RuntimeError(
            f"spaceData body must be {expected_length} bytes, got {len(body)}"
        )
    return bytes([CLIENT_MSG_SPACE_DATA]) + struct.pack("<H", len(body)) + body


def send_player_space_data(base_sock: socket.socket, session: Session,
                           addr: tuple[str, int]) -> None:
    """Map the selected geometry into the PlayerAvatar server space.

    ClientInterface::spaceData is variable-length message ID 0x07.

    Body:
        SpaceID        int32
        SpaceEntryID   uint32 ip + uint16 port + uint16 salt
        key            uint16 = SPACE_DATA_MAPPING_KEY_CLIENT_SERVER
        mappingData    4x4 FLOAT32 matrix followed by raw path bytes

    The path has no trailing NUL because ServerConnection::spaceData consumes
    the complete remaining message body as the data string.
    """
    msg = build_player_space_data_message(session)
    body_length = struct.unpack_from("<H", msg, 1)[0]

    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "player spaceData")
    session.player_space_data_sent = True
    session.player_space_data_seq = seq
    session.last_server_send = time.time()

    log(
        f"TX PLAYER SPACE DATA: reliable seq={seq}, "
        f"msg=0x{CLIENT_MSG_SPACE_DATA:02x}, "
        f"spaceID={session.play_space_id}, "
        f"key={SPACE_DATA_MAPPING_KEY_CLIENT_SERVER}, "
        f"path={session.play_geometry.decode('ascii')!r}, "
        f"body={body_length} bytes, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("PLAYER SPACE DATA clear hex:\n" + hex_dump(clear))
    geometry = session.play_geometry.decode("ascii")
    log(f">>> Stage 19 milestone C: {geometry} geometry mapping sent.")
    log(f">>> Expected client: onGeometryMapped + {geometry}/space.settings.\n")

def send_avatar_dummy_enter(base_sock: socket.socket, session: Session,
                            addr: tuple[str, int]) -> None:
    """Send ONLY ClientInterface::enterAoI for AvatarDummy.

    SOnline's embedded ClientInterface has both createEntity and
    createEntityDetailed. Their confirmed startup IDs are:
        0x08 createEntity
        0x09 createEntityDetailed
        0x0A enterAoI

    Keeping enterAoI in its own reliable packet is intentional. The client can
    ACK it and, on normal BigWorld builds, queue BaseAppExtInterface::
    requestEntityUpdate (client->server message 0x09). This makes the entity
    lifecycle observable instead of hiding two handlers inside one bundle.
    """
    entity_id = session.avatar_dummy_entity_id
    msg = bytes([0x0A]) + struct.pack("<iB", entity_id, 0xFF)
    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "AvatarDummy enterAoI")
    session.avatar_enter_sent = True
    session.avatar_enter_seq = seq
    session.last_server_send = time.time()
    log(
        f"TX AVATAR ENTER: reliable seq={seq}, EntityID={entity_id}, "
        f"alias=0xff, cumAck={session.client_next_expected_seq}"
    )
    log("AVATAR ENTER clear hex:\n" + hex_dump(clear))
    log(">>> Stage 15 milestone E1: enterAoI(AvatarDummy) sent ALONE.")
    log(">>> Expected: client cumulativeAck >= 5; requestEntityUpdate(2) may follow.\n")


def _avatar_dummy_initial_properties(char_index: int = 0) -> bytes:
    """Encode AvatarDummy's initial ALL_CLIENTS property set.

    BigWorld EntityCache::addChangedProperties() writes the create-entity tail as:
        uint8 propertyCount
        repeated { uint8 clientServerPropertyIndex, serializedValue }

    AvatarDummy.def contains exactly one client-visible property:
        charIndex : INT32, Flags=ALL_CLIENTS, Default=0

    Therefore the initial property stream must explicitly contain property index 0
    followed by the little-endian INT32 value.  Sending only ``\x00`` (zero
    properties) was not a faithful createEntityDetailed payload and left the
    CharacterPicker without the server-side AvatarDummy state it expects.
    """
    return b"\x01\x00" + struct.pack("<i", int(char_index))


def send_avatar_dummy_detailed(base_sock: socket.socket, session: Session,
                               addr: tuple[str, int]) -> None:
    """Send SOnline ClientInterface::createEntityDetailed as message 0x09."""
    entity_id = session.avatar_dummy_entity_id
    type_id = session.avatar_dummy_type_id
    create_body = (
        b"\x00"  # BW_COMPRESSION_NONE
        + struct.pack("<iH", entity_id, type_id)
        + struct.pack("<fff", 0.0, 0.0, 0.0)  # Position3D
        + struct.pack("<fff", 0.0, 0.0, 0.0)  # yaw / pitch / roll FLOAT32
        + _avatar_dummy_initial_properties(0)
    )
    msg = bytes([0x09]) + struct.pack("<H", len(create_body)) + create_body
    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "AvatarDummy detailed create")
    session.avatar_detailed_sent = True
    session.avatar_detailed_seq = seq
    session.last_server_send = time.time()
    log(
        f"TX AVATAR DETAILED: reliable seq={seq}, msg=0x09, EntityID={entity_id}, "
        f"EntityTypeID={type_id}, body={len(create_body)} bytes, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("AVATAR DETAILED clear hex:\n" + hex_dump(clear))
    log("AVATAR DETAILED encrypted hex:\n" + hex_dump(encrypted))
    log(">>> Stage 15 milestone E2: createEntityDetailed(AvatarDummy) sent ALONE.")
    log(">>> AvatarDummy properties: count=1, propertyIndex=0, charIndex=0.")
    log(">>> Expected client cumulativeAck >= 6.\n")


def _pack_bigworld_string(value: str) -> bytes:
    """BinaryOStream::appendString compatible UTF-8 string."""
    raw = value.encode("utf-8")
    n = len(raw)
    if n < 0xFF:
        return bytes([n]) + raw
    if n >= (1 << 24):
        raise ValueError("BigWorld string is too long")
    return b"\xff" + bytes((n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF)) + raw


def validate_avatar_name(name: str) -> tuple[str | None, int]:
    """Mirror scripts/common/validators.py AvatarName for the Russian client."""
    name = name.strip()
    if len(name) < 3:
        return None, ACCOUNT_RESPONSE_TOO_SHORT
    if len(name) > 32:
        return None, ACCOUNT_RESPONSE_TOO_LONG

    uid = name.lower()
    # The shipped Russian Account.xml accepts either Cyrillic or Latin, but
    # does not allow mixing the alphabets. Digits and one underscore are okay.
    latin = re.fullmatch(r"[a-z0-9_]*", uid)
    cyrillic = re.fullmatch(r"[а-я0-9_]*", uid)
    if not latin and not cyrillic:
        return None, ACCOUNT_RESPONSE_NOT_ALLOWED_SYMBOLS
    if uid.count("_") > 1:
        return None, ACCOUNT_RESPONSE_TOO_MANY_GROUNDS
    if uid.startswith("_"):
        return None, ACCOUNT_RESPONSE_BEGIN_WITH_GROUND
    if uid.endswith("_"):
        return None, ACCOUNT_RESPONSE_END_WITH_GROUND
    return name, ACCOUNT_RESPONSE_EVERYTHING_OK


def send_name_availability(base_sock: socket.socket, session: Session,
                           addr: tuple[str, int], uid: str,
                           available: bool) -> None:
    """Reply Account.client.onAvatarNameAvailability(uid, available).

    Proven receiveCharacterList mapping gives Account's six inherited client
    methods before its own declarations. receiveCharacterList is own index 8
    -> exposed index 14 -> Mercury 0x8E. onAvatarNameAvailability is own index
    19, therefore exposed index 25 -> Mercury 0x99.
    """
    client_method_index = 25
    mercury_msg_id = 0x80 | client_method_index  # 0x99
    args = _pack_bigworld_string(uid) + bytes([1 if available else 0])
    body = struct.pack("<i", session.account_entity_id) + args
    msg = bytes([mercury_msg_id]) + struct.pack("<H", len(body)) + body

    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "avatar name availability")
    session.last_server_send = time.time()

    log(
        f"TX NAME AVAILABLE: reliable seq={seq}, msg=0x{mercury_msg_id:02x}, "
        f"uid={uid!r}, available={available}, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("NAME AVAILABLE clear hex:\n" + hex_dump(clear))
    log(">>> Account.client.onAvatarNameAvailability reply sent.")
    log(">>> The nickname spinner should stop and Done should become available.")
    log(">>> Press Done; next target is Account.base.createNewAvatar() [0xCB].\n")


def _build_character_info_wire(character: CharacterRecord) -> bytes:
    """Build one CHARACTER_INFO using its persisted MariaDB values.

    alias.xml defines CHARACTER_INFO in this exact order:
      UNICODE_STRING name
      INT32 renamesAvailable
      BOOL renameRequired
      PACKED_AVATAR_MODEL defaultModels   (5 * MODEL_AND_TINT = 60 bytes)
      ARMORSET playerKit                   (9 * {ID INT32, Type INT32})
      INT8 isTutorialPassed
      STATS_VALUES charstats               (6 * FLOAT = 24 bytes)
      INT32 goldCredit
      FLOAT deletion_remaining_time

    createNewAvatar() supplies PACKED_AVATAR_MODEL itself. Persisting those 60
    bytes keeps the exact appearance selected by the client across restarts.
    """
    models = character.models_wire
    if len(models) != 60:
        log(
            f"WARNING: createNewAvatar defaultModels was {len(models)} bytes, "
            "expected 60; using zero PACKED_AVATAR_MODEL fallback"
        )
        models = b"\x00" * 60

    return (
        _pack_bigworld_string(character.name)
        + struct.pack("<i", character.renames_available)
        + bytes([1 if character.rename_required else 0])
        + models
        # AvatarDummy.compileModel() uses character.playerKit when a character
        # is selected. Its own GetDefaultValues() fallback creates every cloth
        # slot as ID=0, Type=1. Sending 18 zero INT32s therefore changed the
        # semantic value of the kit and could make StalkerModel.ComposePlayerModel
        # build an invalid/incomplete model. Mirror the client's real defaults:
        #   Head, Shirt, Hands, Boots, Armor, Pants, Hat, Mask, BackPack
        #   -> each pair is (ID=0, Type=1).
        + character.player_kit_wire
        + struct.pack("<b", character.is_tutorial_passed)
        + character.charstats_wire
        + struct.pack("<i", character.gold_credit)
        + struct.pack("<f", character.deletion_remaining_time)
    )


def send_character_list(base_sock: socket.socket, session: Session,
                        addr: tuple[str, int],
                        characters: list[CharacterRecord]) -> None:
    """Send Account.client.receiveCharacterList() from persistent storage."""
    mercury_msg_id = 0x8E
    msg = build_character_list_message(session, characters)

    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "persistent character list")
    session.character_list_sent = True
    session.character_list_acked = False
    session.character_list_seq = seq
    session.last_server_send = time.time()

    log(
        f"TX CHARACTER LIST: reliable seq={seq}, msg=0x8e, "
        f"characters={len(characters)}, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("CHARACTER LIST clear hex:\n" + hex_dump(clear))
    log(">>> Persistent character list delivered to the picker.\n")


def build_character_list_message(
    session: Session,
    characters: list[CharacterRecord],
) -> bytes:
    character_wires = [_build_character_info_wire(char) for char in characters]
    args = struct.pack("<i", len(character_wires)) + b"".join(character_wires)
    body = struct.pack("<i", session.account_entity_id) + args
    return b"\x8e" + struct.pack("<H", len(body)) + body

def send_create_character_callback(base_sock: socket.socket, session: Session,
                                   addr: tuple[str, int], succeeded: bool = True,
                                   errcode: int = 0) -> None:
    """Reply Account.client.createCharacterCallback(BOOL, INT32).

    Account.def places createCharacterCallback immediately before
    receiveCharacterList. Since receiveCharacterList is exposed index 14
    (Mercury 0x8E), this callback is exposed index 13 (Mercury 0x8D).
    """
    mercury_msg_id = 0x8D
    args = bytes([1 if succeeded else 0]) + struct.pack("<i", errcode)
    body = struct.pack("<i", session.account_entity_id) + args
    msg = bytes([mercury_msg_id]) + struct.pack("<H", len(body)) + body

    clear, encrypted, seq = build_server_channel_packet(
        session, message_bytes=msg, reliable=True
    )
    safe_udp_sendto(base_sock, encrypted, addr, "create character callback")
    session.create_callback_sent = True
    session.create_callback_acked = False
    session.create_callback_succeeded = succeeded
    session.create_callback_seq = seq
    if succeeded:
        session.created_character_list_sent = False
    session.last_server_send = time.time()

    log(
        f"TX CREATE CHARACTER CALLBACK: reliable seq={seq}, msg=0x8d, "
        f"succeeded={succeeded}, errcode={errcode}, "
        f"cumAck={session.client_next_expected_seq}"
    )
    log("CREATE CALLBACK clear hex:\n" + hex_dump(clear))
    log(">>> Stage 15 milestone G: Account.client.createCharacterCallback(True, 0) sent.")
    log(">>> The Create/Done loading state should now finish.")
    log(">>> Any follow-up requestCharacterList/beginPlay RPC will be captured.\n")


def load_and_send_character_list(
    repository: MariaDBRepository,
    base_sock: socket.socket,
    session: Session,
    addr: tuple[str, int],
) -> None:
    characters = repository.list_characters(session.account_id)
    send_character_list(base_sock, session, addr, characters)


def handle_base_channel_packet(data: bytes, addr: tuple[str, int],
                               sessions: list[Session],
                               base_sock: socket.socket,
                               repository: MariaDBRepository) -> None:
    candidates = [
        s for s in reversed(sessions)
        if s.base_logged_in and
        (s.base_client_addr == addr or s.login_client_addr[0] == addr[0])
    ]

    session = None
    plain = None
    for s in candidates:
        try:
            candidate = decrypt_filtered_packet(s.blowfish_key, data)
        except Exception:
            continue
        session = s
        plain = candidate
        break

    if session is None or plain is None:
        flags = struct.unpack_from("<H", data, 0)[0] if len(data) >= 2 else 0
        log("BaseApp channel decrypt: FAILED / packet may be plaintext")
        log(f"Raw flags     : 0x{flags:04x} ({flag_text(flags)})")
        log("Raw packet hex:\n" + hex_dump(data))
        return

    session.base_client_addr = addr
    session.channel_started = True
    session.post_login_packets += 1

    try:
        packet = parse_channel_packet(plain)
    except Exception as exc:
        log(f"BaseApp channel parser: FAILED ({exc})")
        log("Decrypted hex:\n" + hex_dump(plain))
        return

    log("BaseApp channel decrypt: OK")
    log(f"Session user  : {session.username!r}")
    log(f"Server key    : 0x{session.server_session_key:08x}")
    log(f"Post-login pkt: #{session.post_login_packets}")
    log(f"Plain length  : {len(plain)} bytes")
    log(f"Mercury flags : 0x{packet.flags:04x} ({flag_text(packet.flags)})")
    log(f"Sequence      : {packet.sequence}")
    log(f"Cumulative ACK: {packet.cumulative_ack}")
    if packet.acks:
        log(f"Explicit ACKs : {packet.acks}")
    log(f"Message bytes : {packet.message_bytes.hex() or '<empty>'}")
    log("Decrypted hex:\n" + hex_dump(plain))

    # Track reliable client packets. First real SOnline packet is seq 0 and
    # contains authenticate + enableEntities.
    duplicate = False
    if (packet.flags & FLAG_IS_RELIABLE) and packet.sequence is not None:
        expected = session.client_next_expected_seq
        if packet.sequence == expected:
            session.client_next_expected_seq = (
                session.client_next_expected_seq + 1
            ) & 0x0FFFFFFF
        elif packet.sequence < expected:
            duplicate = True
        else:
            log(f"WARNING: reliable gap: got seq={packet.sequence}, expected={expected}")

    found = describe_baseapp_messages(session, packet.message_bytes)

    # Pong is an application-level entity RPC, not a Mercury ACK. Answer it
    # immediately; the reliable Pong packet also carries the cumulative ACK.
    if found["playerPing"]:
        send_player_pong(base_sock, session, addr)
        return

    # Stage 16: CameraNode.py creates the preview AvatarDummy inside the local
    # character-picker space and positions it in front of its camera. A
    # server-side AoI entity would belong to the connection's server space and
    # remain invisible (or conflict with the local preview), so answer the list
    # request directly.
    if found["requestCharacterList"]:
        try:
            load_and_send_character_list(
                repository, base_sock, session, addr
            )
        except Exception as exc:
            log(f"DATABASE ERROR while listing characters: {exc}")
            send_channel_ack(base_sock, session, addr, "character-list DB error")
        return

    # Mercury may bundle the final name check with createNewAvatar. Preserve
    # the request order seen on the wire: createNewAvatar (0xCB) first, then
    # playerCheckAvatarNameAvailability (0xC9). Do not return after answering
    # only one of them or the character-create callback is lost.
    handled_character_rpc = False
    created_now = False
    create_avatar_name = found.get("createAvatarName")
    if isinstance(create_avatar_name, str):
        valid_name, errcode = validate_avatar_name(create_avatar_name)
        succeeded = False
        if valid_name is not None:
            try:
                repository.create_character(
                    session.account_id,
                    valid_name,
                    session.created_default_models_wire,
                )
                session.created_avatar_name = valid_name
                succeeded = True
                created_now = True
                errcode = ACCOUNT_RESPONSE_EVERYTHING_OK
                log(
                    f">>> Character {valid_name!r} persisted for "
                    f"account_id={session.account_id}."
                )
            except CharacterNameTaken:
                errcode = ACCOUNT_RESPONSE_ALREADY_TAKEN
            except NoFreeCharacterSlots:
                errcode = ACCOUNT_RESPONSE_NO_FREE_SLOTS
            except Exception as exc:
                log(f"DATABASE ERROR while creating character: {exc}")
                errcode = ACCOUNT_RESPONSE_NO_SUCH_CHARACTER
        send_create_character_callback(
            base_sock, session, addr, succeeded, errcode
        )
        handled_character_rpc = True

    name_check_uid = found.get("nameCheckUid")
    if isinstance(name_check_uid, str):
        valid_name, _ = validate_avatar_name(name_check_uid)
        available = False
        if valid_name is not None:
            if (
                created_now
                and valid_name.casefold() == session.created_avatar_name.casefold()
            ):
                # The real client can bundle its final name check after the
                # create RPC. Creation already reserved the name, but this
                # reply still belongs to the pre-create validation.
                available = True
            else:
                try:
                    available = repository.is_character_name_available(valid_name)
                except Exception as exc:
                    log(f"DATABASE ERROR while checking character name: {exc}")
        send_name_availability(
            base_sock, session, addr, name_check_uid, available
        )
        handled_character_rpc = True

    if handled_character_rpc:
        return

    delete_avatar_name = found.get("deleteAvatarName")
    if isinstance(delete_avatar_name, str):
        try:
            repository.delete_character(
                session.account_id, delete_avatar_name
            )
            log(f">>> Character {delete_avatar_name!r} marked for deletion.")
            load_and_send_character_list(repository, base_sock, session, addr)
        except CharacterNotFound:
            log(f">>> Delete ignored: character {delete_avatar_name!r} not found.")
            load_and_send_character_list(repository, base_sock, session, addr)
        except Exception as exc:
            log(f"DATABASE ERROR while deleting character: {exc}")
            send_channel_ack(base_sock, session, addr, "delete-character DB error")
        return

    restore_character_name = found.get("restoreCharacterName")
    if isinstance(restore_character_name, str):
        try:
            repository.restore_character(
                session.account_id, restore_character_name
            )
            log(f">>> Character {restore_character_name!r} restored.")
            load_and_send_character_list(repository, base_sock, session, addr)
        except CharacterNotFound:
            log(f">>> Restore ignored: character {restore_character_name!r} not found.")
            load_and_send_character_list(repository, base_sock, session, addr)
        except Exception as exc:
            log(f"DATABASE ERROR while restoring character: {exc}")
            send_channel_ack(base_sock, session, addr, "restore-character DB error")
        return

    begin_play_name = found.get("beginPlayName")
    if isinstance(begin_play_name, str) and not session.player_base_sent:
        try:
            character = repository.get_character(
                session.account_id, begin_play_name
            )
            if character is None:
                log(
                    f">>> beginPlay rejected locally: {begin_play_name!r} "
                    "does not belong to this account or is deleted."
                )
                load_and_send_character_list(repository, base_sock, session, addr)
                return
            configure_player_character(
                session,
                character,
                session.begin_play_tutorial,
            )

            session.active_character_id = character.id

            # Canonical persisted name, not merely the RPC spelling.
            session.begin_play_name = character.name

            session.active_default_models_wire = (
                normalise_avatar_models_wire(
                    character.models_wire
                )
            )

            if not is_valid_world_position(
                session.play_position
            ):
                raise RuntimeError(
                    "beginPlay produced invalid spawn position: "
                    f"{session.play_position!r}"
                )

            # This deliberately rewrites corrupted coordinates as soon
            # as the character is selected.
            repository.set_tutorial_and_location(
                character.id,
                session.play_pass_tutorial,
                session.play_geometry.decode("ascii"),
                session.play_position,
            )

            models_values = struct.unpack(
                "<15i",
                session.active_default_models_wire,
            )

            log(
                f">>> Loaded character_id={character.id}, "
                f"name={character.name!r}, "
                f"world={session.play_geometry.decode('ascii')!r}, "
                f"position={session.play_position!r}, "
                f"passTutorial={session.play_pass_tutorial}, "
                f"defaultModelTypeIDs="
                f"{models_values[2::3]!r}."
            )

        except Exception as exc:
            log(
                f"DATABASE/BOOTSTRAP ERROR during beginPlay: {exc}"
            )
            send_channel_ack(
                base_sock,
                session,
                addr,
                "beginPlay bootstrap error",
            )
            return

        send_avatar_base_player(
            base_sock,
            session,
            addr,
        )
        return

    if (
        session.create_callback_sent
        and not session.create_callback_acked
        and session.create_callback_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= session.create_callback_seq + 1
    ):
        session.create_callback_acked = True
        if session.create_callback_succeeded and not session.created_character_list_sent:
            session.created_character_list_due = time.time() + 0.25
        log(
            f">>> CREATE CHARACTER CALLBACK ACK confirmed: "
            f"cumulativeAck={packet.cumulative_ack}"
        )
        if session.create_callback_succeeded:
            log(">>> Persistent character-list refresh scheduled in 0.25 s.\n")
        if not packet.message_bytes:
            return

    if (
        session.character_list_sent
        and not session.character_list_acked
        and session.character_list_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= session.character_list_seq + 1
    ):
        session.character_list_acked = True
        log(
            f">>> CHARACTER LIST ACK confirmed by client: "
            f"cumulativeAck={packet.cumulative_ack}"
        )
        log(">>> Stage 16 character list ACK: client-local preview can now open.\n")
        if not packet.message_bytes:
            return

    # Stage 15 E1: standalone enterAoI ACK.
    if (
        session.avatar_enter_sent
        and not session.avatar_enter_acked
        and session.avatar_enter_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= session.avatar_enter_seq + 1
    ):
        session.avatar_enter_acked = True
        if not session.avatar_detailed_sent:
            session.avatar_create_due = time.time() + 0.20
        log(f">>> AVATAR ENTER ACK confirmed: cumulativeAck={packet.cumulative_ack}")
        log(">>> createEntityDetailed(0x09) scheduled in 0.20 s.\n")
        if not packet.message_bytes:
            return

    if found.get("requestEntityUpdate") and session.avatar_enter_sent:
        if not session.avatar_detailed_sent:
            session.avatar_create_due = min(
                session.avatar_create_due or (time.time() + 0.05),
                time.time() + 0.05,
            )
        log(">>> ENTER AOI CONFIRMED BY CLIENT requestEntityUpdate.")
        log(">>> detailed create accelerated to +0.05 s.\n")

    # Stage 15 E2: a single detailed create is authoritative.  Stage 15's
    # same-ID 0x08 fallback is intentionally gone: the real client reported
    # "AvatarDummy 2 has been destroyed" when CharacterPicker later selected it.
    if (
        session.avatar_detailed_sent
        and not session.avatar_detailed_acked
        and session.avatar_detailed_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= session.avatar_detailed_seq + 1
    ):
        session.avatar_detailed_acked = True
        session.character_list_due = time.time() + 0.25
        log(f">>> AVATAR DETAILED ACK confirmed: cumulativeAck={packet.cumulative_ack}")
        log(">>> Stage 15: NO same-ID 0x08 fallback will be sent.")
        log(">>> receiveCharacterList([]) scheduled in 0.25 s.\n")
        if not packet.message_bytes:
            return

    # Install the persisted appearance on the base PlayerAvatar before it
    # enters the cell. PlayerAvatar.onEnterWorld composes its model immediately,
    # so a property update after createCellPlayer is too late for the first
    # model build.
    if (
        session.player_base_sent
        and not session.player_base_acked
        and session.player_base_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack
        >= session.player_base_seq + 1
    ):
        session.player_base_acked = True
        session.player_cell_due = time.time() + 0.25

        log(
            ">>> STAGE 20 PLAYERAVATAR BOOTSTRAP ACK: "
            f"cumulativeAck={packet.cumulative_ack}"
        )
        log(
            ">>> createBasePlayer + name + defaultModels "
            "accepted by client."
        )
        log(
            ">>> createCellPlayer scheduled in 0.25 s.\n"
        )

        if not packet.message_bytes:
            return
    
    if (
        session.player_cell_sent
        and not session.player_cell_acked
        and session.player_cell_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= session.player_cell_seq + 1
    ):
        session.player_cell_acked = True
        log(f">>> AVATAR CELL PLAYER ACK confirmed: cumulativeAck={packet.cumulative_ack}")
        log(">>> Stage 19: createCellPlayer accepted; setting passTutorial now.\n")
        if not session.player_tutorial_property_sent:
            send_player_pass_tutorial(base_sock, session, addr)
        return

    if (
        session.player_tutorial_property_sent
        and not session.player_tutorial_property_acked
        and session.player_tutorial_property_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= session.player_tutorial_property_seq + 1
    ):
        session.player_tutorial_property_acked = True
        log(
            f">>> AVATAR passTutorial ACK confirmed: "
            f"cumulativeAck={packet.cumulative_ack}"
        )
        log(
            f">>> Mapping {session.play_geometry.decode('ascii')} now.\n"
        )
        if not session.player_space_data_sent:
            send_player_space_data(base_sock, session, addr)
        return

    if (
        session.player_space_data_sent
        and not session.player_space_data_acked
        and session.player_space_data_seq >= 0
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= session.player_space_data_seq + 1
    ):
        session.player_space_data_acked = True
        log(f">>> PLAYER SPACE DATA ACK confirmed: cumulativeAck={packet.cumulative_ack}")
        log(
            f">>> Stage 19 transport complete: "
            f"{session.play_geometry.decode('ascii')} mapping accepted by client.\n"
        )
        return

    # Stage 10 startup state machine.
    #
    # 1) Client sends authenticate + enableEntities.
    # 2) Server sends reliable authenticate (seq 0).
    # 3) Client ACKs it with cumulativeAck >= 1.
    # 4) Server sends timing init in its OWN reliable packet (seq 1).
    # 5) Client ACKs it with cumulativeAck >= 2.
    # 6) Account creation is scheduled shortly afterwards as seq 2.
    #
    # The separate init packet is deliberate: real BaseApp implementations
    # flush updateFrequency/tickSync/setGameTime before CREATE_BASE_PLAYER.

    if found["enableEntities"] and not session.server_auth_sent:
        log("\n>>> Stage 10 milestone A: client authenticate + enableEntities decoded.")
        send_server_auth(base_sock, session, addr)
        log(">>> Server authenticate sent as reliable packet seq=0.\n")
        return

    if (
        session.server_auth_sent
        and not session.client_init_sent
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= 1
    ):
        log(
            f">>> Server-auth ACK confirmed by client: "
            f"cumulativeAck={packet.cumulative_ack}"
        )
        send_client_init(base_sock, session, addr)
        return

    if (
        session.client_init_sent
        and not session.client_init_acked
        and packet.cumulative_ack is not None
        and packet.cumulative_ack >= 2
    ):
        session.client_init_acked = True
        session.account_create_due = time.time() + 0.75
        log(
            f">>> CLIENT INIT ACK confirmed: cumulativeAck={packet.cumulative_ack}"
        )
        log(
            ">>> CREATE ACCOUNT scheduled in 0.75 s. "
            "No extra packet is inserted before it.\n"
        )
        return

    send_channel_ack(
        base_sock, session, addr,
        "duplicate reliable packet" if duplicate else "channel traffic"
    )



def parse_login_request(data: bytes) -> LoginRequest:
    if len(data) < 17:
        raise ValueError("datagram is too short")
    flags = struct.unpack_from("<H", data, 0)[0]
    if not (flags & FLAG_HAS_REQUESTS):
        raise ValueError(f"expected HAS_REQUESTS, got flags=0x{flags:04x}")

    first_request_offset = struct.unpack_from("<H", data, len(data) - 2)[0]
    message_end = len(data) - 2
    off = first_request_offset
    if off < 2 or off + 9 > message_end:
        raise ValueError(f"invalid first request offset {off}")

    message_id = data[off]
    body_length = struct.unpack_from("<H", data, off + 1)[0]
    reply_id = struct.unpack_from("<i", data, off + 3)[0]
    next_request_offset = struct.unpack_from("<H", data, off + 7)[0]
    body_off = off + 9
    body_end = body_off + body_length
    if body_end > message_end:
        raise ValueError(
            f"message body overruns datagram: body_end={body_end}, message_end={message_end}"
        )
    if body_length < 4:
        raise ValueError("login body is shorter than uint32 LOGIN_VERSION")

    login_version = struct.unpack_from("<I", data, body_off)[0]
    rsa_payload = data[body_off + 4:body_end]
    return LoginRequest(
        flags, message_id, body_length, reply_id, next_request_offset,
        first_request_offset, login_version, rsa_payload
    )


def mgf1_sha1(seed: bytes, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hashlib.sha1(seed + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:length])


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def rsa_oaep_sha1_decrypt(ciphertext: bytes, key_file: Path) -> bytes:
    cfg = json.loads(key_file.read_text(encoding="ascii"))
    n = int(cfg["n"], 16)
    d = int(cfg["d"], 16)
    k = (n.bit_length() + 7) // 8
    if len(ciphertext) != k:
        raise ValueError(f"RSA block is {len(ciphertext)} bytes, expected {k}")
    c = int.from_bytes(ciphertext, "big")
    if c >= n:
        raise ValueError("RSA ciphertext representative out of range")
    em = pow(c, d, n).to_bytes(k, "big")

    hlen = hashlib.sha1().digest_size
    if len(em) < 2 * hlen + 2 or em[0] != 0:
        raise ValueError("invalid RSA-OAEP encoded message")
    masked_seed = em[1:1 + hlen]
    masked_db = em[1 + hlen:]
    seed = xor_bytes(masked_seed, mgf1_sha1(masked_db, hlen))
    db = xor_bytes(masked_db, mgf1_sha1(seed, k - hlen - 1))
    lhash = hashlib.sha1(b"").digest()
    if db[:hlen] != lhash:
        raise ValueError("RSA-OAEP label hash mismatch")
    rest = db[hlen:]
    try:
        one = rest.index(1)
    except ValueError as exc:
        raise ValueError("RSA-OAEP separator not found") from exc
    if any(rest[:one]):
        raise ValueError("RSA-OAEP padding string is not zero-filled")
    return rest[one + 1:]


def read_packed_string(data: bytes, off: int) -> tuple[bytes, int]:
    if off >= len(data):
        raise ValueError("truncated packed string length")
    n = data[off]
    off += 1
    if n == 0xFF:
        if off + 3 > len(data):
            raise ValueError("truncated 24-bit packed string length")
        n = data[off] | (data[off + 1] << 8) | (data[off + 2] << 16)
        off += 3
    if off + n > len(data):
        raise ValueError("packed string overruns plaintext")
    return data[off:off + n], off + n


def parse_logon_params(clear: bytes) -> LogOnParams:
    if not clear:
        raise ValueError("empty LogOnParams plaintext")
    off = 0
    flags = clear[off]
    off += 1
    username_b, off = read_packed_string(clear, off)
    password_b, off = read_packed_string(clear, off)
    encryption_key, off = read_packed_string(clear, off)
    digest = b""
    if flags & 0x01:
        if off + 16 > len(clear):
            raise ValueError("truncated MD5 digest")
        digest = clear[off:off + 16]
        off += 16
    if off + 4 > len(clear):
        raise ValueError("truncated nonce")
    nonce = struct.unpack_from("<I", clear, off)[0]
    off += 4
    return LogOnParams(
        flags,
        username_b.decode("utf-8", errors="replace"),
        password_b.decode("utf-8", errors="replace"),
        encryption_key,
        digest,
        nonce,
        clear[off:],
    )


def pack_bw_string(value: str) -> bytes:
    raw = value.encode("utf-8")
    n = len(raw)
    if n < 0xFF:
        return bytes([n]) + raw
    if n >= (1 << 24):
        raise ValueError("BigWorld string is too long")
    return b"\xff" + bytes((n & 0xff, (n >> 8) & 0xff, (n >> 16) & 0xff)) + raw


def bf_cipher(key: bytes) -> Cipher:
    return Cipher(Blowfish(key), modes.ECB())


def bf_ecb_encrypt(key: bytes, block: bytes) -> bytes:
    enc = bf_cipher(key).encryptor()
    return enc.update(block) + enc.finalize()


def bf_ecb_decrypt(key: bytes, block: bytes) -> bytes:
    dec = bf_cipher(key).decryptor()
    return dec.update(block) + dec.finalize()


def bw_blowfish_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """BigWorld EncryptionFilter::encrypt() block chaining."""
    if len(plaintext) % BLOWFISH_BLOCK:
        raise ValueError("Blowfish plaintext length must be multiple of 8")
    out = bytearray()
    prev_plain = None
    for off in range(0, len(plaintext), BLOWFISH_BLOCK):
        plain = plaintext[off:off + BLOWFISH_BLOCK]
        mixed = plain if prev_plain is None else xor_bytes(plain, prev_plain)
        out.extend(bf_ecb_encrypt(key, mixed))
        prev_plain = plain
    return bytes(out)


def bw_blowfish_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """Inverse of BigWorld EncryptionFilter::encrypt()."""
    if len(ciphertext) % BLOWFISH_BLOCK:
        raise ValueError("encrypted packet size is not multiple of 8")
    out = bytearray()
    prev_plain = None
    for off in range(0, len(ciphertext), BLOWFISH_BLOCK):
        block = ciphertext[off:off + BLOWFISH_BLOCK]
        mixed = bf_ecb_decrypt(key, block)
        plain = mixed if prev_plain is None else xor_bytes(mixed, prev_plain)
        out.extend(plain)
        prev_plain = plain
    return bytes(out)


def encrypt_login_reply_record(key: bytes, host: str, port: int, session_key: int) -> tuple[bytes, bytes]:
    # Mercury::Address stream = raw IPv4 + raw network-order port + uint16 salt.
    record = socket.inet_aton(host) + struct.pack(">H", port) + struct.pack("<H", 0)
    record += struct.pack("<I", session_key)
    # EncryptionFilter::encryptStream pads with zero bytes to an 8-byte boundary.
    pad = (-len(record)) % BLOWFISH_BLOCK
    clear_padded = record + (b"\x00" * pad)
    return bw_blowfish_encrypt(key, clear_padded), record


def build_reply(reply_id: int, payload: bytes) -> bytes:
    body = struct.pack("<i", reply_id) + payload
    return struct.pack("<H", 0) + bytes([REPLY_MESSAGE_ID]) + struct.pack("<I", len(body)) + body


def build_login_failure_reply(reply_id: int, status: int, description: str) -> bytes:
    return build_reply(reply_id, bytes([status & 0xFF]) + pack_bw_string(description))


def build_login_success_reply(reply_id: int, blowfish_key: bytes, base_host: str,
                              base_port: int, session_key: int) -> tuple[bytes, bytes, bytes]:
    encrypted_record, clear_record = encrypt_login_reply_record(
        blowfish_key, base_host, base_port, session_key
    )
    packet = build_reply(reply_id, bytes([LOGGED_ON]) + encrypted_record)
    return packet, clear_record, encrypted_record


def encrypt_filtered_packet(key: bytes, clear_packet: bytes) -> bytes:
    """Apply BigWorld Mercury::EncryptionFilter packet framing + Blowfish."""
    base_len = len(clear_packet) + 4
    wastage = ((BLOWFISH_BLOCK - ((base_len + 1) % BLOWFISH_BLOCK)) % BLOWFISH_BLOCK) + 1
    total_len = base_len + wastage

    buf = bytearray(total_len)
    buf[:len(clear_packet)] = clear_packet

    magic_off = total_len - 1 - 4
    struct.pack_into("<I", buf, magic_off, ENCRYPTION_MAGIC)
    buf[-1] = wastage

    return bw_blowfish_encrypt(key, bytes(buf))


def decrypt_filtered_packet(key: bytes, ciphertext: bytes) -> bytes:
    clear = bw_blowfish_decrypt(key, ciphertext)
    if len(clear) < 5:
        raise ValueError("decrypted packet too short")
    wastage = clear[-1]
    magic = struct.unpack_from("<I", clear, len(clear) - 5)[0]
    if magic != ENCRYPTION_MAGIC:
        raise ValueError(f"bad encryption magic 0x{magic:08x}")
    footer_size = wastage + 4
    if wastage < 1 or wastage > BLOWFISH_BLOCK or footer_size > len(clear):
        raise ValueError(f"illegal wastage={wastage}")
    return clear[:-footer_size]


def find_u32(data: bytes, value: int) -> list[int]:
    needle = struct.pack("<I", value)
    out = []
    start = 0
    while True:
        i = data.find(needle, start)
        if i < 0:
            break
        out.append(i)
        start = i + 1
    return out


def parse_plain_baseapp_header(plain: bytes) -> None:
    if len(plain) >= 2:
        flags = struct.unpack_from("<H", plain, 0)[0]
        log(f"Base flags    : 0x{flags:04x} ({flag_text(flags)})")
    else:
        return


def main() -> None:
    ap = argparse.ArgumentParser(description="SOEmulator Stage 18 - gameplay Ping/Pong")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--login-port", type=int, default=22231)
    ap.add_argument("--base-host", default="127.0.0.1")
    ap.add_argument("--base-port", type=int, default=22232)
    ap.add_argument("--key", type=Path, default=DEFAULT_RSA_JSON)
    ap.add_argument("--db-host", default=os.getenv("SOEMU_DB_HOST", "127.0.0.1"))
    ap.add_argument("--db-port", type=int, default=int(os.getenv("SOEMU_DB_PORT", "3307")))
    ap.add_argument("--db-user", default=os.getenv("SOEMU_DB_USER", "root"))
    ap.add_argument("--db-name", default=os.getenv("SOEMU_DB_NAME", "soemu"))
    ap.add_argument(
        "--world-mode",
        choices=("auto", "station", "lubech"),
        default="auto",
        help=(
            "initial world: auto follows beginPlay tutorial flag; station and "
            "lubech are explicit recovery overrides"
        ),
    )
    ap.add_argument("--show-password", action="store_true")
    ap.add_argument("--dump-login-hex", action="store_true")
    args = ap.parse_args()

    if not args.key.is_file():
        raise SystemExit(f"Missing RSA key data: {args.key}")

    LOG_PATH.write_text("", encoding="utf-8")

    db_password = os.getenv("SOEMU_DB_PASSWORD")
    if db_password is None:
        db_password = getpass.getpass(
            f"MariaDB password for {args.db_user}@{args.db_host}:{args.db_port}: "
        )
    repository = MariaDBRepository(MariaDBConfig(
        host=args.db_host,
        port=args.db_port,
        user=args.db_user,
        password=db_password,
        database=args.db_name,
    ))
    try:
        repository.initialise()
    except Exception as exc:
        raise SystemExit(
            f"MariaDB initialisation failed at {args.db_host}:{args.db_port}: {exc}"
        ) from exc

    login_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    login_sock.bind((args.host, args.login_port))
    base_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    base_sock.bind((args.host, args.base_port))

    sessions: list[Session] = []

    log("SOEmulator stage 18")
    log(f"LoginApp : UDP {args.host}:{args.login_port}")
    log(f"BaseApp  : UDP {args.host}:{args.base_port}")
    log(f"Client will be redirected to {args.base_host}:{args.base_port}")
    log(
        f"MariaDB : {args.db_user}@{args.db_host}:{args.db_port}/"
        f"{args.db_name} (password not logged)"
    )
    log(f"SOnline login protocol: {LOGIN_VERSION}")
    log(
        "Mode: beginPlay tutorial routing + gameplay Ping/Pong "
        f"(world-mode={args.world_mode})"
    )
    log("Ctrl+C to stop.\n")

    try:
        while True:
            readable, _, _ = select.select([login_sock, base_sock], [], [], 0.10)
            for sock in readable:
                try:
                    data, addr = sock.recvfrom(65535)
                except OSError as exc:
                    if _is_udp_peer_reset(exc):
                        log("UDP peer reset (WinError 10054), continuing")
                        continue
                    raise
                now = time.strftime("%Y-%m-%d %H:%M:%S")

                if sock is login_sock:
                    log(f"\n[{now}] LOGIN RX {addr[0]}:{addr[1]} -> {len(data)} bytes")
                    try:
                        req = parse_login_request(data)
                    except Exception as exc:
                        log(f"LOGIN PARSE ERROR: {exc}")
                        log(hex_dump(data))
                        continue

                    log(f"Mercury flags : 0x{req.flags:04x} ({flag_text(req.flags)})")
                    log(f"Message ID    : {req.message_id}")
                    log(f"Message length: {req.body_length}")
                    log(f"Reply ID      : {req.reply_id}")
                    log(f"Login version : {req.login_version}")

                    if req.message_id != LOGIN_MESSAGE_ID:
                        log("Ignoring non-login message on LoginApp socket")
                        continue
                    if req.login_version != LOGIN_VERSION:
                        reply = build_login_failure_reply(
                            req.reply_id, LOGIN_BAD_PROTOCOL_VERSION,
                            f"SOEmulator expects login protocol {LOGIN_VERSION}"
                        )
                        safe_udp_sendto(login_sock, reply, addr, "bad-version login reply")
                        log("TX LOGIN_BAD_PROTOCOL_VERSION")
                        continue

                    try:
                        clear = rsa_oaep_sha1_decrypt(req.rsa_payload, args.key)
                        params = parse_logon_params(clear)
                    except Exception as exc:
                        log(f"RSA/LogOnParams ERROR: {exc}")
                        reply = build_login_failure_reply(
                            req.reply_id, LOGIN_MALFORMED_REQUEST,
                            "SOEmulator could not decode LogOnParams"
                        )
                        safe_udp_sendto(login_sock, reply, addr, "malformed login reply")
                        continue

                    log("RSA decrypt   : OK")
                    log(f"Username      : {params.username!r}")
                    if args.show_password:
                        log(f"Password      : {params.password!r}")
                    else:
                        log(f"Password      : {'*' * len(params.password)} ({len(params.password)} chars)")
                    log(f"Session cipher: {len(params.encryption_key)} bytes / {params.encryption_key.hex()}")
                    if not (4 <= len(params.encryption_key) <= 56):
                        log("ERROR: invalid Blowfish key length")
                        continue

                    try:
                        account = repository.authenticate_or_create(
                            params.username, params.password
                        )
                    except InvalidCredentials:
                        reply = build_login_failure_reply(
                            req.reply_id,
                            LOGIN_REJECTED_INVALID_PASSWORD,
                            "Invalid account password",
                        )
                        safe_udp_sendto(login_sock, reply, addr, "invalid-password reply")
                        log(f"TX LOGIN_REJECTED_INVALID_PASSWORD for {params.username!r}")
                        continue
                    except InvalidAccountName as exc:
                        reply = build_login_failure_reply(
                            req.reply_id,
                            LOGIN_REJECTED_ILLEGAL_CHARACTERS,
                            str(exc),
                        )
                        safe_udp_sendto(login_sock, reply, addr, "invalid-account-name reply")
                        log(f"TX LOGIN_REJECTED_ILLEGAL_CHARACTERS: {exc}")
                        continue
                    except Exception as exc:
                        reply = build_login_failure_reply(
                            req.reply_id,
                            LOGIN_REJECTED_DB_GENERAL_FAILURE,
                            "Account database is unavailable",
                        )
                        safe_udp_sendto(login_sock, reply, addr, "account DB failure reply")
                        log(f"TX LOGIN_REJECTED_DB_GENERAL_FAILURE: {exc}")
                        continue

                    log(
                        f"Account DB    : id={account.id}, "
                        f"{'created' if account.created else 'authenticated'}"
                    )

                    # One loginKey is enough for our local emulator. Generate a fresh uint32.
                    login_session_key = int.from_bytes(os.urandom(4), "little") or 1
                    success, clear_record, encrypted_record = build_login_success_reply(
                        req.reply_id,
                        params.encryption_key,
                        args.base_host,
                        args.base_port,
                        login_session_key,
                    )
                    safe_udp_sendto(login_sock, success, addr, "successful login reply")
                    sessions.append(Session(
                        username=account.username,
                        account_id=account.id,
                        blowfish_key=params.encryption_key,
                        login_session_key=login_session_key,
                        login_client_addr=addr,
                        created_at=time.time(),
                        world_mode=args.world_mode,
                    ))
                    # Keep only recent sessions; retries may create duplicates.
                    sessions[:] = [s for s in sessions if time.time() - s.created_at < 120][-16:]

                    log(f"TX LOGGED_ON  : {len(success)} bytes")
                    log(f"BaseApp target: {args.base_host}:{args.base_port}")
                    log(f"Login key     : 0x{login_session_key:08x}")
                    log(f"ReplyRecord   : {clear_record.hex()} ({len(clear_record)} bytes)")
                    log(f"Encrypted rec : {encrypted_record.hex()} ({len(encrypted_record)} bytes)")
                    if args.dump_login_hex:
                        log("LOGIN TX hex:\n" + hex_dump(success))

                else:
                    log(f"\n[{now}] BASEAPP RX {addr[0]}:{addr[1]} -> {len(data)} bytes")

                    try:
                        breq = parse_baseapp_login_request(data)
                    except Exception as exc:
                        # Once baseAppLogin succeeds the same socket becomes the normal channel.
                        log(f"Not a baseAppLogin request ({exc})")
                        handle_base_channel_packet(
                            data, addr, sessions, base_sock, repository
                        )
                        continue

                    log(f"Mercury flags : 0x{breq.flags:04x} ({flag_text(breq.flags)})")
                    log(f"Message ID    : {breq.message_id} (baseAppLogin)")
                    log(f"Message length: {breq.body_length}")
                    log(f"Reply ID      : {breq.reply_id}")
                    log(f"First req off : {breq.first_request_offset}")
                    log(f"Next req off  : {breq.next_request_offset}")
                    log(f"Login key     : 0x{breq.login_key:08x}")
                    log(f"Attempt       : {breq.attempt}")

                    matched: Session | None = None
                    for session in reversed(sessions):
                        if session.login_session_key == breq.login_key:
                            matched = session
                            break

                    if matched is None:
                        log("BASEAPP LOGIN REJECTED LOCALLY: unknown login key")
                        log("Packet hex:\n" + hex_dump(data))
                        continue

                    # The BaseApp reply body is a single SessionKey uint32.
                    # Reuse the same generated server key for retries of this login.
                    if matched.server_session_key == 0:
                        matched.server_session_key = int.from_bytes(os.urandom(4), "little") or 1

                    clear_reply = build_reply(
                        breq.reply_id,
                        struct.pack("<I", matched.server_session_key)
                    )
                    encrypted_reply = encrypt_filtered_packet(
                        matched.blowfish_key, clear_reply
                    )
                    safe_udp_sendto(base_sock, encrypted_reply, addr, "baseAppLogin reply")

                    matched.base_client_addr = addr
                    matched.base_logged_in = True

                    log(f"Session user  : {matched.username!r}")
                    log(f"Server key    : 0x{matched.server_session_key:08x}")
                    log(f"TX BASEAPP OK : {len(encrypted_reply)} encrypted bytes to {addr[0]}:{addr[1]}")
                    log(f"Clear reply   : {len(clear_reply)} bytes")
                    log("Clear reply hex:\n" + hex_dump(clear_reply))
                    log("Encrypted reply hex:\n" + hex_dump(encrypted_reply))
                    log("\n>>> Stage 9 login milestone: encrypted baseAppLogin SUCCESS reply sent.")
                    log(">>> If accepted, attempts 1..9 must STOP.")
                    log(">>> The next BaseApp packets should be real encrypted channel traffic.\n")

            now_ts = time.time()

            # CREATE_BASE_PLAYER is intentionally emitted from the timer path,
            # not synchronously while the client's ACK datagram is still being
            # handled.  This gives the client main loop a clean boundary after
            # its timing initialization packet.
            for session in sessions:
                if (
                    session.client_init_acked
                    and not session.account_create_sent
                    and session.account_create_due > 0.0
                    and now_ts >= session.account_create_due
                    and session.base_client_addr is not None
                ):
                    send_create_base_player(
                        base_sock, session, session.base_client_addr
                    )

            # Legacy Stage 15 AvatarDummy timers remain below for trace
            # compatibility, but are dormant in Stage 16 because no enterAoI is
            # scheduled. The picker preview is a client-local entity.
            for session in sessions:
                if (
                    session.avatar_enter_sent
                    and not session.avatar_detailed_sent
                    and session.avatar_create_due > 0.0
                    and now_ts >= session.avatar_create_due
                    and session.base_client_addr is not None
                ):
                    send_avatar_dummy_detailed(
                        base_sock, session, session.base_client_addr
                    )

                if (
                    session.avatar_detailed_acked
                    and not session.character_list_sent
                    and session.character_list_due > 0.0
                    and now_ts >= session.character_list_due
                    and session.base_client_addr is not None
                ):
                    try:
                        load_and_send_character_list(
                            repository, base_sock, session, session.base_client_addr
                        )
                    except Exception as exc:
                        log(f"DATABASE ERROR in character-list timer: {exc}")

                if (
                    session.player_base_acked
                    and not session.player_cell_sent
                    and session.player_cell_due > 0.0
                    and now_ts >= session.player_cell_due
                    and session.base_client_addr is not None
                ):
                    send_avatar_cell_player(
                        base_sock,
                        session,
                        session.base_client_addr,
                    )

                if (
                    session.create_callback_acked
                    and session.create_callback_succeeded
                    and session.created_avatar_name
                    and not session.created_character_list_sent
                    and session.created_character_list_due > 0.0
                    and now_ts >= session.created_character_list_due
                    and session.base_client_addr is not None
                ):
                    try:
                        load_and_send_character_list(
                            repository, base_sock, session, session.base_client_addr
                        )
                        session.created_character_list_sent = True
                    except Exception as exc:
                        log(f"DATABASE ERROR in post-create list timer: {exc}")

                if (
                    session.active_character_id
                    and session.position_dirty
                    and now_ts - session.last_position_save >= 5.0
                ):
                    if not is_valid_world_position(
                        session.play_position
                    ):
                        log(
                            "STAGE 20: dirty position rejected before DB save: "
                            f"{session.play_position!r}"
                        )
                        session.position_dirty = False
                        continue

                    try:
                        repository.update_position(
                            session.active_character_id,
                            session.play_geometry.decode("ascii"),
                            session.play_position,
                        )
                        session.position_dirty = False
                        session.last_position_save = now_ts
                    except Exception as exc:
                        log(
                            "DATABASE ERROR while saving position: "
                            f"{exc}"
                        )

            # Keep established BaseApp channels alive using the separate
            # non-reliable sequence space confirmed by the real client.
            for session in sessions:
                if (
                    session.base_logged_in
                    and session.channel_started
                    and session.base_client_addr is not None
                    and now_ts - session.last_server_send >= 10.0
                ):
                    send_channel_ack(
                        base_sock,
                        session,
                        session.base_client_addr,
                        "10s keepalive",
                    )

    except KeyboardInterrupt:
        log("\nStopped.")
    finally:
        for session in sessions:
            for session in sessions:
            if (
                session.active_character_id
                and session.position_dirty
                and is_valid_world_position(
                    session.play_position
                )
            ):
                try:
                    repository.update_position(
                        session.active_character_id,
                        session.play_geometry.decode("ascii"),
                        session.play_position,
                    )
                except Exception as exc:
                    log(
                        "DATABASE ERROR during final position save: "
                        f"{exc}"
                    )
        login_sock.close()
        base_sock.close()


if __name__ == "__main__":
    main()
