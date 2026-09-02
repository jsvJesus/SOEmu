from __future__ import annotations

import ast
import pickle
import re
import struct
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


CLIENT_FLAGS = {
    "OTHER_CLIENTS",
    "OWN_CLIENT",
    "BASE_AND_CLIENT",
    "CELL_PUBLIC_AND_OWN",
    "ALL_CLIENTS",
}

BASE_PLAYER_FLAGS = {"BASE_AND_CLIENT"}

CELL_PLAYER_FLAGS = {
    "ALL_CLIENTS",
    "OTHER_CLIENTS",
    "OWN_CLIENT",
    "CELL_PUBLIC_AND_OWN",
}


_XML_INVALID_CONTROL_CHARS = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f]"
)

_XML_COMMENTS = re.compile(
    r"<!--.*?-->",
    re.DOTALL,
)

_XML_BARE_AMPERSAND = re.compile(
    r"&(?!"
    r"#\d+;"
    r"|#x[0-9a-fA-F]+;"
    r"|amp;"
    r"|lt;"
    r"|gt;"
    r"|apos;"
    r"|quot;"
    r")"
)


@dataclass(frozen=True)
class TypeField:
    name: str
    type_spec: "TypeSpec"
    default_node: ET.Element | None


@dataclass(frozen=True)
class TypeSpec:
    kind: str
    item_type: "TypeSpec | None" = None
    fields: tuple[TypeField, ...] = ()
    fixed_size: int = 0


@dataclass(frozen=True)
class PropertyDef:
    name: str
    flags: str
    type_spec: TypeSpec
    default_node: ET.Element | None


def _node_text(node: ET.Element | None) -> str:
    if node is None or node.text is None:
        return ""
    return node.text.strip()


def _load_bigworld_xml(path: Path) -> ET.Element:
    raw = path.read_bytes()

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1251")

    # Старые SOnline/BigWorld .def иногда содержат мусорные
    # управляющие байты, которые BigWorld терпит, а ElementTree нет.
    text = _XML_INVALID_CONTROL_CHARS.sub("", text)

    # Комментарии для построения property layout нам вообще не нужны.
    # Удаляем их до XML parse, чтобы старый мусор внутри комментариев
    # не ломал ElementTree.
    text = _XML_COMMENTS.sub("", text)

    # BigWorld resource parser более терпим к голому '&'.
    # Для стандартного XML его необходимо экранировать.
    text = _XML_BARE_AMPERSAND.sub("&amp;", text)

    try:
        return ET.fromstring(text)

    except ET.ParseError as exc:
        line, column = exc.position
        lines = text.splitlines()

        source_line = ""
        if 1 <= line <= len(lines):
            source_line = lines[line - 1]

        raise RuntimeError(
            "invalid BigWorld entity definition XML: "
            f"{path} "
            f"(line {line}, column {column})\n"
            f"source: {source_line!r}"
        ) from exc


def _pack_bigworld_string_bytes(raw: bytes) -> bytes:
    size = len(raw)

    if size < 0xFF:
        return bytes([size]) + raw

    if size >= (1 << 24):
        raise ValueError(
            "BigWorld string exceeds 24-bit packed length"
        )

    return (
        b"\xff"
        + bytes(
            (
                size & 0xFF,
                (size >> 8) & 0xFF,
                (size >> 16) & 0xFF,
            )
        )
        + raw
    )


class AvatarEntityDefinition:
    """
    Avatar entity-def reader required by STAGE 20.

    It does two things:

      1. reproduces BigWorld clientServer property ordering so that
         Avatar.name/defaultModels/passTutorial receive their real
         clientServer indexes;

      2. serializes the complete BASE_AND_CLIENT stream used by
         createBasePlayer and the complete cell/client stream used by
         createCellPlayer.

    Non-client BASE/CELL properties are deliberately left unparsed because
    neither player-creation message sends them to the client.
    """

    def __init__(self, defs_root: Path, entity_name: str = "Avatar"):
        self.defs_root = defs_root
        self.interfaces_root = defs_root / "interfaces"
        self.entity_name = entity_name

        alias_path = defs_root / "alias.xml"

        if not alias_path.is_file():
            raise RuntimeError(
                f"entity alias.xml not found: {alias_path}"
            )

        alias_root = _load_bigworld_xml(alias_path)

        self.aliases: dict[str, ET.Element] = {
            child.tag.strip(): child
            for child in list(alias_root)
            if isinstance(child.tag, str)
        }

        self.properties: dict[str, PropertyDef] = {}
        self.property_order: list[str] = []
        self.client_property_order: list[str] = []

        # Prevent pathological recursive interface loops from taking
        # down the emulator.
        self._interface_stack: list[Path] = []

        self._parse_entity(entity_name)

        if not self.property_order:
            raise RuntimeError(
                f"{entity_name}.def produced no properties"
            )

    @property
    def client_property_count(self) -> int:
        return len(self.client_property_order)

    @property
    def base_property_names(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in self.property_order
            if self.properties[name].flags in BASE_PLAYER_FLAGS
        )

    @property
    def cell_player_property_names(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in self.property_order
            if self.properties[name].flags in CELL_PLAYER_FLAGS
        )

    def client_property_index(self, name: str) -> int:
        try:
            return self.client_property_order.index(name)
        except ValueError as exc:
            raise RuntimeError(
                f"{self.entity_name} property {name!r} is not client-visible"
            ) from exc

    def property_flags(self, name: str) -> str:
        try:
            return self.properties[name].flags
        except KeyError as exc:
            raise RuntimeError(
                f"{self.entity_name} property {name!r} was not found"
            ) from exc

    def build_tagged_client_properties(
        self,
        wire_overrides: dict[str, bytes],
    ) -> bytes:
        """Build EntityCache's count/index/value initial-property stream.

        ``createEntityDetailed`` applies this sparse stream on top of the
        client-side defaults from the entity definition.  This lets world
        entities send only authoritative spawn values while retaining the
        exact clientServer property indexes inherited through interfaces.
        """
        if len(wire_overrides) > 0xFF:
            raise RuntimeError("too many tagged client properties")

        tagged: list[tuple[int, bytes]] = []

        for name, value in wire_overrides.items():
            index = self.client_property_index(name)

            if index > 0xFF:
                raise RuntimeError(
                    f"{self.entity_name} property {name!r} index {index} "
                    "does not fit createEntityDetailed"
                )

            tagged.append((index, bytes(value)))

        tagged.sort(key=lambda item: item[0])
        out = bytearray([len(tagged)])

        for index, value in tagged:
            out.append(index)
            out.extend(value)

        return bytes(out)

    def build_base_player_stream(
        self,
        wire_overrides: dict[str, bytes] | None = None,
    ) -> bytes:
        """
        EntityType::newEntity(BASE_PLAYER_DATA) with a non-empty stream
        reads properties matching BASE_DATA|CLIENT_DATA|EXACT_MATCH.

        For entity defs that corresponds to BASE_AND_CLIENT.
        """
        return self._build_property_stream(
            BASE_PLAYER_FLAGS,
            wire_overrides,
        )

    def build_cell_player_stream(
        self,
        wire_overrides: dict[str, bytes] | None = None,
    ) -> bytes:
        """Serialize CELL_DATA|CLIENT_DATA|EXACT_MATCH properties."""
        return self._build_property_stream(
            CELL_PLAYER_FLAGS,
            wire_overrides,
        )

    def _build_property_stream(
        self,
        flags: set[str],
        wire_overrides: dict[str, bytes] | None,
    ) -> bytes:
        overrides = wire_overrides or {}
        expected_names = {
            name
            for name in self.property_order
            if self.properties[name].flags in flags
        }
        unknown = set(overrides) - expected_names

        if unknown:
            raise RuntimeError(
                "property wire override has the wrong data domain: "
                + ", ".join(sorted(unknown))
            )

        out = bytearray()

        for name in self.property_order:
            prop = self.properties[name]

            if prop.flags not in flags:
                continue

            override = overrides.get(name)

            if override is not None:
                out.extend(override)
                continue

            try:
                out.extend(
                    self._encode_value(
                        prop.type_spec,
                        prop.default_node,
                    )
                )
            except Exception as exc:
                raise RuntimeError(
                    "failed to serialize Avatar client property "
                    f"property {name!r}: {exc}"
                ) from exc

        if not out:
            raise RuntimeError(
                "Avatar player property data unexpectedly "
                "serialized to zero bytes"
            )

        return bytes(out)

    def _parse_entity(self, entity_name: str) -> None:
        path = self.defs_root / f"{entity_name}.def"

        if not path.is_file():
            raise RuntimeError(
                f"entity definition not found: {path}"
            )

        root = _load_bigworld_xml(path)

        parent_name = _node_text(root.find("Parent"))

        if parent_name:
            self._parse_entity(parent_name)

        self._parse_interface_root(
            root,
            source_path=path,
        )

    def _parse_interface_root(
        self,
        root: ET.Element,
        source_path: Path | None = None,
    ) -> None:
        implements = root.find("Implements")

        if implements is not None:
            for interface_node in list(implements):
                interface_name = _node_text(interface_node)

                if not interface_name:
                    continue

                path = (
                    self.interfaces_root
                    / f"{interface_name}.def"
                )

                if not path.is_file():
                    raise RuntimeError(
                        "Avatar interface definition "
                        f"not found: {path}"
                    )

                resolved = path.resolve()

                if resolved in self._interface_stack:
                    chain = " -> ".join(
                        str(item)
                        for item in (
                            *self._interface_stack,
                            resolved,
                        )
                    )
                    raise RuntimeError(
                        "recursive Avatar interface chain: "
                        f"{chain}"
                    )

                self._interface_stack.append(resolved)

                try:
                    interface_root = _load_bigworld_xml(path)

                    self._parse_interface_root(
                        interface_root,
                        source_path=path,
                    )
                finally:
                    self._interface_stack.pop()

        properties_node = root.find("Properties")

        if properties_node is None:
            return

        for prop_node in list(properties_node):
            if not isinstance(prop_node.tag, str):
                continue

            name = prop_node.tag.strip()
            flags = _node_text(
                prop_node.find("Flags")
            )

            type_node = prop_node.find("Type")

            if type_node is None:
                raise RuntimeError(
                    f"property {name!r} has no <Type> "
                    f"in {source_path}"
                )

            # For property indexes we only need name + flags + order.
            #
            # Player creation streams contain both the base/client and
            # cell/client domains, so every client-visible property needs
            # a concrete type even if ordinary property updates are not
            # currently emitted for it.
            if flags in CLIENT_FLAGS:
                type_spec = self._parse_type(type_node)
            else:
                type_spec = TypeSpec("UNUSED")

            prop = PropertyDef(
                name=name,
                flags=flags,
                type_spec=type_spec,
                default_node=prop_node.find("Default"),
            )

            old = self.properties.get(name)

            if old is None:
                self.property_order.append(name)

                if flags in CLIENT_FLAGS:
                    self.client_property_order.append(name)

            else:
                old_client = old.flags in CLIENT_FLAGS
                new_client = flags in CLIENT_FLAGS

                # BigWorld keeps the original property slot on an
                # override. For a normal client-visible -> client-visible
                # override our existing index is therefore preserved.
                if old_client and not new_client:
                    raise RuntimeError(
                        f"property {name!r} changes from "
                        f"client-visible {old.flags} to {flags}"
                    )

                if new_client and not old_client:
                    self.client_property_order.append(name)

            self.properties[name] = prop

    def _parse_type(
        self,
        node: ET.Element,
    ) -> TypeSpec:
        text = _node_text(node)

        if not text:
            raise RuntimeError(
                f"empty type specification in <{node.tag}>"
            )

        kind = text.split()[0].strip().upper()

        alias = self.aliases.get(kind)

        if alias is not None:
            return self._parse_type(alias)

        if kind == "BOOL":
            return TypeSpec("UINT8")

        if kind in {
            "INT8",
            "UINT8",
            "INT16",
            "UINT16",
            "INT32",
            "UINT32",
            "INT64",
            "UINT64",
            "FLOAT",
            "FLOAT32",
            "FLOAT64",
            "STRING",
            "UNICODE_STRING",
            "BLOB",
            "VECTOR2",
            "VECTOR3",
            "VECTOR4",
            "PYTHON",
            "MAILBOX",
        }:
            return TypeSpec(kind)

        if kind in {"ARRAY", "TUPLE"}:
            of_node = node.find("of")

            if of_node is None:
                raise RuntimeError(
                    f"{kind} has no <of> type"
                )

            size_node = node.find("size")
            fixed_size = 0

            if size_node is not None:
                size_text = _node_text(size_node)

                if size_text:
                    fixed_size = int(size_text, 0)

            return TypeSpec(
                kind=kind,
                item_type=self._parse_type(of_node),
                fixed_size=fixed_size,
            )

        if kind in {"FIXED_DICT", "CLASS"}:
            properties_node = node.find(
                "Properties"
            )

            if properties_node is None:
                raise RuntimeError(
                    f"{kind} has no <Properties>"
                )

            fields: list[TypeField] = []

            for field_node in list(properties_node):
                if not isinstance(
                    field_node.tag,
                    str,
                ):
                    continue

                field_type_node = (
                    field_node.find("Type")
                )

                if field_type_node is None:
                    raise RuntimeError(
                        f"{kind}.{field_node.tag} "
                        "has no <Type>"
                    )

                fields.append(
                    TypeField(
                        name=field_node.tag.strip(),
                        type_spec=self._parse_type(
                            field_type_node
                        ),
                        default_node=field_node.find(
                            "Default"
                        ),
                    )
                )

            return TypeSpec(
                kind=kind,
                fields=tuple(fields),
            )

        raise RuntimeError(
            f"unsupported BigWorld data type {kind!r}"
        )

    def _encode_value(
        self,
        spec: TypeSpec,
        default_node: ET.Element | None,
    ) -> bytes:
        kind = spec.kind
        text = _node_text(default_node)

        if kind == "INT8":
            return struct.pack(
                "<b",
                int(text or "0", 0),
            )

        if kind == "UINT8":
            return struct.pack(
                "<B",
                int(text or "0", 0),
            )

        if kind == "INT16":
            return struct.pack(
                "<h",
                int(text or "0", 0),
            )

        if kind == "UINT16":
            return struct.pack(
                "<H",
                int(text or "0", 0),
            )

        if kind == "INT32":
            return struct.pack(
                "<i",
                int(text or "0", 0),
            )

        if kind == "UINT32":
            return struct.pack(
                "<I",
                int(text or "0", 0),
            )

        if kind == "INT64":
            return struct.pack(
                "<q",
                int(text or "0", 0),
            )

        if kind == "UINT64":
            return struct.pack(
                "<Q",
                int(text or "0", 0),
            )

        if kind in {"FLOAT", "FLOAT32"}:
            return struct.pack(
                "<f",
                float(text or "0"),
            )

        if kind == "FLOAT64":
            return struct.pack(
                "<d",
                float(text or "0"),
            )

        if kind in {
            "STRING",
            "UNICODE_STRING",
        }:
            return _pack_bigworld_string_bytes(
                text.encode("utf-8")
            )

        if kind == "BLOB":
            raw = (
                text.encode("latin1")
                if text
                else b""
            )

            return _pack_bigworld_string_bytes(
                raw
            )

        if kind.startswith("VECTOR"):
            count = int(kind[-1])

            values = self._parse_vector(
                default_node,
                count,
            )

            return struct.pack(
                "<" + ("f" * count),
                *values,
            )

        if kind in {"ARRAY", "TUPLE"}:
            if spec.item_type is None:
                raise RuntimeError(
                    f"{kind} has no item type"
                )

            values: list[ET.Element | None]

            if (
                default_node is not None
                and list(default_node)
            ):
                values = list(default_node)
            else:
                values = []

            if spec.fixed_size:
                if not values:
                    values = (
                        [None]
                        * spec.fixed_size
                    )

                elif len(values) != spec.fixed_size:
                    raise RuntimeError(
                        f"{kind} default has "
                        f"{len(values)} entries, "
                        f"expected {spec.fixed_size}"
                    )

            out = bytearray()

            if spec.fixed_size == 0:
                out.extend(
                    struct.pack(
                        "<i",
                        len(values),
                    )
                )

            for value_node in values:
                out.extend(
                    self._encode_value(
                        spec.item_type,
                        value_node,
                    )
                )

            return bytes(out)

        if kind in {"FIXED_DICT", "CLASS"}:
            out = bytearray()

            for field in spec.fields:
                value_node = None

                if default_node is not None:
                    value_node = (
                        default_node.find(
                            field.name
                        )
                    )

                if value_node is None:
                    value_node = (
                        field.default_node
                    )

                out.extend(
                    self._encode_value(
                        field.type_spec,
                        value_node,
                    )
                )

            return bytes(out)

        if kind == "PYTHON":
            if not text:
                value = None
            else:
                try:
                    value = ast.literal_eval(text)
                except Exception:
                    value = text

            raw = pickle.dumps(
                value,
                protocol=2,
            )

            return _pack_bigworld_string_bytes(
                raw
            )

        raise RuntimeError(
            f"cannot serialize unsupported "
            f"type {kind!r}"
        )

    @staticmethod
    def _parse_vector(
        node: ET.Element | None,
        count: int,
    ) -> tuple[float, ...]:
        if node is None:
            return tuple(
                0.0
                for _ in range(count)
            )

        children = list(node)

        if children:
            values = [
                float(
                    _node_text(child)
                    or "0"
                )
                for child in children[:count]
            ]

        else:
            raw = _node_text(node)

            parts = [
                part
                for part in re.split(
                    r"[\s,]+",
                    raw,
                )
                if part
            ]

            values = [
                float(part)
                for part in parts
            ]

        values.extend(
            0.0
            for _ in range(
                count - len(values)
            )
        )

        return tuple(
            values[:count]
        )
