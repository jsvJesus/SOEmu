"""Spawn the original so_origins tutorial NPCs through BigWorld's client API.

Only the marshalled onGeometryMapped code, constants and names are extended.
Keeping the rest of the Python 2.6 marshal stream byte-for-byte intact is
required because rebuilding this large code object with a modern marshaller
produces a file that the embedded interpreter rejects during startup.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path
from typing import Any

from xdis.load import load_module
from xdis.opcodes import opcode_26


MARKER = "SOEMU_TUTORIAL_NPCS_V6"

# The original server-side BaseNPCPoint/BaseTraderPoint data is absent from
# so_origins.  These placements are reconstructed from stable map landmarks:
# the station counters, the fireplace behind the Kamaz and the draisine.
TUTORIAL_NPCS = (
    ("Zevaka", (-68.804001, -1.499511, 117.475388), -3.030917,
     {"npcHead": 6, "npcBody": 0, "npcLegs": 1}),
    ("Soldat_Noob", (-61.9033, -2.4801, 87.0193), -2.468817,
     {"npcWeapon": 2, "npcHead": 49, "npcBody": 39,
      "npcHands": 0, "npcLegs": 0, "npcBoots": 0}),
    ("Dejurnyi", (32.5, 4.862886, 61.0), -0.709703,
     {"npcWeapon": 2, "npcHead": 49, "npcBody": 39,
      "npcHands": 0, "npcLegs": 0, "npcBoots": 0}),
    ("Trader_Noob", (36.02113, 4.862886, 58.851074), -0.194092,
     {"npcHead": 0, "npcHands": 0, "npcBoots": 0,
      "npcBody": 45, "npcLegs": 0}),
    ("Aid_trader_noob", (30.8758, 4.862886, 55.0822), -0.755271,
     {"npcHead": 10, "npcHands": 0, "npcBoots": 0,
      "npcBody": 48, "npcLegs": 0}),
    ("Repairman_Noob", (27.1875, 4.862886, 59.3451), -0.805763,
     {"npcHead": 0, "npcHands": 0, "npcBoots": 0,
      "npcBody": 57, "npcLegs": 0}),
    ("Ammo_trader_noob", (36.4713, 4.862886, 72.3113), -2.292016,
     {"npcHead": 8, "npcBody": 41, "npcLegs": 2}),
    ("Armor_trader_noob", (43.3354, 4.862886, 72.0319), 2.896250,
     {"npcHead": 11, "npcBody": 44, "npcLegs": 2}),
    ("Provodnik_Noob", (201.561188, 3.800753, 228.807495), 0.373340,
     {"npcHead": 10, "npcBody": 9, "npcLegs": 2}),
    ("Haron_Corpse", (177.12561, 1.726031, 128.862808), 3.049426,
     {"npcHead": 13, "npcBody": 0, "npcLegs": 1,
      "npcFlags": 1, "dead": 1}),
)

DEFAULT_PROPERTIES = {
    "npcType": 1,
    "actionOnLaunch": "",
    "npcWeapon": 0,
    "npcHead": 1,
    "npcHands": 1,
    "npcBoots": 1,
    "npcBody": 1,
    "npcArmor": 0,
    "npcLegs": 1,
    "npcCap": 0,
    "npcMask": 0,
    "npcBackpack": 0,
    "npcFlags": 3,
    "clanName": "",
    "fractionID": 0,
    "headTrackerEnable": 1,
}


def _instruction(opcode: int, argument: int | None = None) -> bytes:
    if argument is None:
        return bytes((opcode,))
    if not 0 <= argument <= 0xFFFF:
        raise ValueError(f"Python 2.6 opcode argument out of range: {argument}")
    return bytes((opcode, argument & 0xFF, argument >> 8))


def _find_method(code: Any, method_name: str) -> Any:
    if getattr(code, "co_name", None) == method_name:
        return code
    for constant in code.co_consts:
        if hasattr(constant, "co_consts"):
            found = _find_method(constant, method_name)
            if found is not None:
                return found
    return None


def _skip_marshaled(data: bytes, offset: int) -> int:
    """Return the first byte after one Python 2 marshal value."""
    kind = data[offset:offset + 1]
    offset += 1

    if kind in b"0N.FTSx":
        return offset
    if kind in b"iR":
        return offset + 4
    if kind == b"I":
        return offset + 8
    if kind == b"l":
        digits = struct.unpack_from("<i", data, offset)[0]
        return offset + 4 + abs(digits) * 2
    if kind in (b"f", b"x"):
        length = data[offset]
        return offset + 1 + length
    if kind == b"g":
        return offset + 8
    if kind == b"y":
        return offset + 16
    if kind in (b"s", b"t", b"u"):
        length = struct.unpack_from("<i", data, offset)[0]
        return offset + 4 + length
    if kind in (b"(", b"[", b"<", b">"):
        count = struct.unpack_from("<i", data, offset)[0]
        offset += 4
        for _ in range(count):
            offset = _skip_marshaled(data, offset)
        return offset
    if kind == b"{":
        while data[offset:offset + 1] != b"0":
            offset = _skip_marshaled(data, offset)
            offset = _skip_marshaled(data, offset)
        return offset + 1
    raise RuntimeError(
        f"Unsupported marshal type {kind!r} at offset {offset - 1}"
    )


def _tuple_end(data: bytes, offset: int, expected_count: int) -> int:
    if data[offset:offset + 1] != b"(":
        raise RuntimeError(f"Expected marshal tuple at offset {offset}")
    count = struct.unpack_from("<i", data, offset + 1)[0]
    if count != expected_count:
        raise RuntimeError(
            f"Marshal tuple count mismatch: expected {expected_count}, got {count}"
        )
    end = offset + 5
    for _ in range(count):
        end = _skip_marshaled(data, end)
    return end


def _marshal_constant(value: object) -> bytes:
    if type(value) is str:
        encoded = value.encode("ascii")
        return b"s" + struct.pack("<i", len(encoded)) + encoded
    if type(value) is int:
        return b"i" + struct.pack("<i", value)
    if type(value) is float:
        return b"g" + struct.pack("<d", value)
    raise TypeError(f"Unsupported injected constant: {value!r}")


def _build_injection(method: Any) -> tuple[bytes, tuple[object, ...], tuple[str, ...]]:
    constants = list(method.co_consts)
    names = list(method.co_names)

    def constant_index(value: object) -> int:
        for index, current in enumerate(constants):
            if type(current) is type(value) and current == value:
                return index
        constants.append(value)
        return len(constants) - 1

    def name_index(value: str) -> int:
        if value not in names:
            names.append(value)
        return names.index(value)

    load_const = lambda value: _instruction(
        opcode_26.LOAD_CONST, constant_index(value)
    )
    load_name = lambda value: _instruction(
        opcode_26.LOAD_GLOBAL, name_index(value)
    )
    load_attr = lambda value: _instruction(
        opcode_26.LOAD_ATTR, name_index(value)
    )

    injected = bytearray()
    injected += load_const(MARKER)
    injected += _instruction(opcode_26.PRINT_ITEM)
    injected += _instruction(opcode_26.PRINT_NEWLINE)

    for npc_name, position, yaw, overrides in TUTORIAL_NPCS:
        properties = dict(DEFAULT_PROPERTIES)
        properties.update(overrides)
        properties["npcName"] = npc_name

        injected += load_const("SOEMU_NPC_GROUND")
        injected += _instruction(opcode_26.PRINT_ITEM)
        injected += load_const(npc_name)
        injected += _instruction(opcode_26.PRINT_ITEM)

        injected += load_name("BigWorld")
        injected += load_attr("createEntity")
        injected += load_const("NPC")
        injected += _instruction(opcode_26.LOAD_FAST, 0)
        injected += load_attr("spaceID")
        injected += load_const(0)

        # Resolve the feet position from collision when this NPC's chunk is
        # loaded. Distant chunks return None during initial geometry mapping,
        # so fall back to the map-derived position instead of aborting the
        # remainder of the roster.
        injected += load_name("BigWorld")
        injected += load_attr("collide")
        injected += _instruction(opcode_26.LOAD_FAST, 0)
        injected += load_attr("spaceID")
        for coordinate in (position[0], position[1] + 1.0, position[2]):
            injected += load_const(float(coordinate))
        injected += _instruction(opcode_26.BUILD_TUPLE, 3)
        for coordinate in (position[0], position[1] - 10.0, position[2]):
            injected += load_const(float(coordinate))
        injected += _instruction(opcode_26.BUILD_TUPLE, 3)
        injected += _instruction(opcode_26.CALL_FUNCTION, 3)

        fallback = bytearray()
        fallback += _instruction(opcode_26.POP_TOP)
        for coordinate in position:
            fallback += load_const(float(coordinate))
        fallback += _instruction(opcode_26.BUILD_TUPLE, 3)
        fallback += _instruction(opcode_26.BUILD_TUPLE, 1)
        injected += _instruction(opcode_26.JUMP_IF_TRUE, len(fallback))
        injected += fallback

        injected += load_const(0)
        injected += _instruction(opcode_26.BINARY_SUBSCR)
        injected += _instruction(opcode_26.DUP_TOP)
        injected += _instruction(opcode_26.PRINT_ITEM)
        injected += _instruction(opcode_26.PRINT_NEWLINE)

        for angle in (0.0, 0.0, float(yaw)):
            injected += load_const(angle)
        injected += _instruction(opcode_26.BUILD_TUPLE, 3)

        injected += _instruction(opcode_26.BUILD_MAP, len(properties))
        for key, value in properties.items():
            injected += load_const(value)
            injected += load_const(key)
            injected += _instruction(opcode_26.STORE_MAP)

        injected += _instruction(opcode_26.CALL_FUNCTION, 6)
        injected += _instruction(opcode_26.POP_TOP)

    return bytes(injected), tuple(constants), tuple(names)


def patch(path: Path) -> bool:
    module_code = load_module(str(path))[3]
    method = _find_method(module_code, "onGeometryMapped")
    if method is None:
        raise RuntimeError("PlayerAvatar.onGeometryMapped was not found")
    if MARKER in method.co_consts:
        print(f"Already patched: {path}")
        return False

    expected_tail = _instruction(opcode_26.LOAD_CONST, 0) + _instruction(
        opcode_26.RETURN_VALUE
    )
    if not method.co_code.endswith(expected_tail) or method.co_consts[0] is not None:
        raise RuntimeError("Unexpected PlayerAvatar.onGeometryMapped bytecode tail")

    data = path.read_bytes()
    code_value = b"s" + struct.pack("<i", len(method.co_code)) + method.co_code
    code_offset = data.find(code_value)
    if code_offset < 0 or data.count(code_value) != 1:
        raise RuntimeError("Could not uniquely locate onGeometryMapped marshal code")

    constants_offset = code_offset + len(code_value)
    constants_end = _tuple_end(data, constants_offset, len(method.co_consts))
    names_offset = constants_end
    names_end = _tuple_end(data, names_offset, len(method.co_names))

    injected, new_constants, new_names = _build_injection(method)
    new_code = method.co_code[:-len(expected_tail)] + injected + expected_tail

    added_constants = new_constants[len(method.co_consts):]
    new_constants_value = (
        b"("
        + struct.pack("<i", len(new_constants))
        + data[constants_offset + 5:constants_end]
        + b"".join(_marshal_constant(value) for value in added_constants)
    )
    added_names = new_names[len(method.co_names):]
    new_names_value = (
        b"("
        + struct.pack("<i", len(new_names))
        + data[names_offset + 5:names_end]
        + b"".join(_marshal_constant(value) for value in added_names)
    )

    prefix = bytearray(data[:code_offset])
    # CPython 2.6 marshal stores stacksize four bytes before co_flags.
    struct.pack_into(
        "<i", prefix, code_offset - 8, max(method.co_stacksize, 12)
    )

    patched = (
        bytes(prefix)
        + b"s" + struct.pack("<i", len(new_code)) + new_code
        + new_constants_value
        + new_names_value
        + data[names_end:]
    )
    path.write_bytes(patched)
    print(f"Patched client tutorial NPC spawning: {path}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "packs"
        / "res"
        / "scripts"
        / "client"
        / "PlayerAvatar.pyc",
    )
    args = parser.parse_args()
    patch(args.path.resolve())


if __name__ == "__main__":
    main()
