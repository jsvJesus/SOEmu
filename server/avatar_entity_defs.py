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


def _pack_bigworld_string_bytes(raw: bytes) -> bytes:
    size = len(raw)

    if size < 0xFF:
        return bytes([size]) + raw

    if size >= (1 << 24):
        raise ValueError("BigWorld string exceeds 24-bit packed length")

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
    def __init__(self, defs_root: Path):
        self.defs_root = defs_root
        self.interfaces_root = defs_root / "interfaces"

        alias_path = defs_root / "alias.xml"
        if not alias_path.is_file():
            raise RuntimeError(f"entity alias.xml not found: {alias_path}")

        alias_root = ET.parse(alias_path).getroot()
        self.aliases: dict[str, ET.Element] = {
            child.tag.strip(): child
            for child in list(alias_root)
            if isinstance(child.tag, str)
        }

        self.properties: dict[str, PropertyDef] = {}
        self.property_order: list[str] = []
        self.client_property_order: list[str] = []

        self._parse_entity("Avatar")

        if not self.property_order:
            raise RuntimeError("Avatar.def produced no properties")

    @property
    def client_property_count(self) -> int:
        return len(self.client_property_order)

    @property
    def base_property_names(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in self.property_order
            if self.properties[name].flags == "BASE_AND_CLIENT"
        )

    def client_property_index(self, name: str) -> int:
        try:
            return self.client_property_order.index(name)
        except ValueError as exc:
            raise RuntimeError(
                f"Avatar property {name!r} is not client-visible"
            ) from exc

    def property_flags(self, name: str) -> str:
        try:
            return self.properties[name].flags
        except KeyError as exc:
            raise RuntimeError(
                f"Avatar property {name!r} was not found"
            ) from exc

    def build_base_player_stream(self) -> bytes:
        out = bytearray()

        for name in self.property_order:
            prop = self.properties[name]

            if prop.flags != "BASE_AND_CLIENT":
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
                    "failed to serialize Avatar BASE_AND_CLIENT "
                    f"property {name!r}: {exc}"
                ) from exc

        if not out:
            raise RuntimeError(
                "Avatar BASE_PLAYER_DATA unexpectedly serialized to zero bytes"
            )

        return bytes(out)

    def _parse_entity(self, entity_name: str) -> None:
        path = self.defs_root / f"{entity_name}.def"

        if not path.is_file():
            raise RuntimeError(f"entity definition not found: {path}")

        root = ET.parse(path).getroot()

        parent_name = _node_text(root.find("Parent"))
        if parent_name:
            self._parse_entity(parent_name)

        self._parse_interface_root(root)

    def _parse_interface_root(self, root: ET.Element) -> None:
        implements = root.find("Implements")

        if implements is not None:
            for interface_node in list(implements):
                interface_name = _node_text(interface_node)
                if not interface_name:
                    continue

                path = self.interfaces_root / f"{interface_name}.def"
                if not path.is_file():
                    raise RuntimeError(
                        f"Avatar interface definition not found: {path}"
                    )

                interface_root = ET.parse(path).getroot()
                self._parse_interface_root(interface_root)

        properties_node = root.find("Properties")
        if properties_node is None:
            return

        for prop_node in list(properties_node):
            if not isinstance(prop_node.tag, str):
                continue

            name = prop_node.tag.strip()
            flags = _node_text(prop_node.find("Flags"))

            type_node = prop_node.find("Type")
            if type_node is None:
                raise RuntimeError(
                    f"property {name!r} has no <Type>"
                )

            prop = PropertyDef(
                name=name,
                flags=flags,
                type_spec=self._parse_type(type_node),
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

                if old_client and not new_client:
                    raise RuntimeError(
                        f"property {name!r} changes from client-visible "
                        f"{old.flags} to {flags}"
                    )

                if new_client and not old_client:
                    self.client_property_order.append(name)

            self.properties[name] = prop

    def _parse_type(self, node: ET.Element) -> TypeSpec:
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
            properties_node = node.find("Properties")

            if properties_node is None:
                raise RuntimeError(
                    f"{kind} has no <Properties>"
                )

            fields: list[TypeField] = []

            for field_node in list(properties_node):
                if not isinstance(field_node.tag, str):
                    continue

                field_type_node = field_node.find("Type")
                if field_type_node is None:
                    raise RuntimeError(
                        f"{kind}.{field_node.tag} has no <Type>"
                    )

                fields.append(
                    TypeField(
                        name=field_node.tag.strip(),
                        type_spec=self._parse_type(field_type_node),
                        default_node=field_node.find("Default"),
                    )
                )

            return TypeSpec(
                kind=kind,
                fields=tuple(fields),
            )

        raise RuntimeError(f"unsupported BigWorld data type {kind!r}")

    def _encode_value(
        self,
        spec: TypeSpec,
        default_node: ET.Element | None,
    ) -> bytes:
        kind = spec.kind

        text = _node_text(default_node)

        if kind == "INT8":
            return struct.pack("<b", int(text or "0", 0))

        if kind == "UINT8":
            return struct.pack("<B", int(text or "0", 0))

        if kind == "INT16":
            return struct.pack("<h", int(text or "0", 0))

        if kind == "UINT16":
            return struct.pack("<H", int(text or "0", 0))

        if kind == "INT32":
            return struct.pack("<i", int(text or "0", 0))

        if kind == "UINT32":
            return struct.pack("<I", int(text or "0", 0))

        if kind == "INT64":
            return struct.pack("<q", int(text or "0", 0))

        if kind == "UINT64":
            return struct.pack("<Q", int(text or "0", 0))

        if kind in {"FLOAT", "FLOAT32"}:
            return struct.pack("<f", float(text or "0"))

        if kind == "FLOAT64":
            return struct.pack("<d", float(text or "0"))

        if kind in {"STRING", "UNICODE_STRING"}:
            return _pack_bigworld_string_bytes(
                text.encode("utf-8")
            )

        if kind == "BLOB":
            raw = text.encode("latin1") if text else b""
            return _pack_bigworld_string_bytes(raw)

        if kind.startswith("VECTOR"):
            count = int(kind[-1])
            values = self._parse_vector(default_node, count)
            return struct.pack("<" + ("f" * count), *values)

        if kind in {"ARRAY", "TUPLE"}:
            if spec.item_type is None:
                raise RuntimeError(f"{kind} has no item type")

            values: list[ET.Element | None]

            if default_node is not None and list(default_node):
                values = list(default_node)
            else:
                values = []

            if spec.fixed_size:
                if not values:
                    values = [None] * spec.fixed_size
                elif len(values) != spec.fixed_size:
                    raise RuntimeError(
                        f"{kind} default has {len(values)} entries, "
                        f"expected {spec.fixed_size}"
                    )

            out = bytearray()

            if spec.fixed_size == 0:
                out.extend(struct.pack("<i", len(values)))

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
                    value_node = default_node.find(field.name)

                if value_node is None:
                    value_node = field.default_node

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

            raw = pickle.dumps(value, protocol=2)
            return _pack_bigworld_string_bytes(raw)

        raise RuntimeError(
            f"cannot serialize unsupported type {kind!r}"
        )

    @staticmethod
    def _parse_vector(
        node: ET.Element | None,
        count: int,
    ) -> tuple[float, ...]:
        if node is None:
            return tuple(0.0 for _ in range(count))

        children = list(node)
        if children:
            values = [
                float(_node_text(child) or "0")
                for child in children[:count]
            ]
        else:
            raw = _node_text(node)
            parts = [
                part
                for part in re.split(r"[\s,]+", raw)
                if part
            ]
            values = [float(part) for part in parts]

        values.extend(
            0.0 for _ in range(count - len(values))
        )

        return tuple(values[:count])