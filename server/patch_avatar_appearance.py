"""Patch the 0.6.5.3 client so persisted character appearance is respected.

The shipped Python 2.6 bytecode reads PACKED_AVATAR_MODEL.type_id and then
discards it in favour of hard-coded clothes/head defaults. Valid type IDs must
win, while zero keeps the original per-slot fallback. The patch changes only
the target function's marshalled code string.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


OLD_CODE = bytes.fromhex(
    "680500740000690100640100367400006902006402003674000069030064030036"
    "74000069040064040036740000690500640500367d01006800007d020078d8007c"
    "0000690600830000445dca005c02007d03007d04007c01007c0300197d05007c04"
    "00640600197d06007c03006401006a02006f150001740700690800640700197c02"
    "007c05003c6e0100017c03006402006a02006f150001740000690900640800197c"
    "02007c05003c6e0100017c03006404006a02006f150001740000690a0064080019"
    "7c02007c05003c6e0100017c03006403006a02006f150001740000690b00640800"
    "197c02007c05003c6e0100017c03006405006a02006f150001740000690c006408"
    "00197c02007c05003c714b0001714b00577c020053"
)

NEW_CODE = bytes.fromhex(
    "680500740000690100640100367400006902006402003674000069030064030036"
    "74000069040064040036740000690500640500367d01006800007d020078d8007c"
    "0000690600830000445dca005c02007d03007d04007c01007c0300197d05007c04"
    "00640600197d06007c03006401006a02006f1500017407006908007c0006197c02"
    "007c05003c6e0100017c03006402006a02006f1500017c0006090909090909097c"
    "02007c05003c6e0100017c03006404006a02006f1500017c000609090909090909"
    "7c02007c05003c6e0100017c03006403006a02006f1500017c0006090909090909"
    "097c02007c05003c6e0100017c03006405006a02006f1500017c00060909090909"
    "09097c02007c05003c714b0001714b00577c020053"
)

# An early development version encoded Python 2.6's two-byte LOAD_FAST
# argument in display order instead of its actual little-endian byte order.
# Recognising it here makes the patch self-repairing if that version was run.
BROKEN_CODE = NEW_CODE
NEW_CODE = BROKEN_CODE.replace(bytes.fromhex("7c0006"), bytes.fromhex("7c0600"))


def _build_fallback_code() -> bytes:
    replacements = {
        # head: heads.preset_by_headid[type_id or 27]
        (126, 130): bytes.fromhex(
            "7c06007004000164070019"
        ),
        # clothes: type_id or the original ItemsCatalog slot fallback.
        (154, 164): bytes.fromhex(
            "7c0600700b000174000069090064080019"
        ),
        (188, 198): bytes.fromhex(
            "7c0600700b0001740000690a0064080019"
        ),
        (222, 232): bytes.fromhex(
            "7c0600700b0001740000690b0064080019"
        ),
        (256, 266): bytes.fromhex(
            "7c0600700b0001740000690c0064080019"
        ),
    }

    ranges = sorted(replacements)

    def relocated(offset: int) -> int:
        return offset + sum(
            len(replacements[(start, end)]) - (end - start)
            for start, end in ranges
            if end <= offset
        )

    output = bytearray()
    cursor = 0

    for start, end in ranges:
        output.extend(NEW_CODE[cursor:start])
        output.extend(replacements[(start, end)])
        cursor = end

    output.extend(NEW_CODE[cursor:])

    relative_jumps = {93, 110, 111, 112, 120}
    absolute_jumps = {113, 119}
    offset = 0

    while offset < len(NEW_CODE):
        opcode = NEW_CODE[offset]
        size = 3 if opcode >= 90 else 1

        if not any(start <= offset < end for start, end in ranges):
            new_offset = relocated(offset)

            if opcode in relative_jumps:
                argument = int.from_bytes(
                    NEW_CODE[offset + 1:offset + 3],
                    "little",
                )
                old_target = offset + size + argument
                new_target = relocated(old_target)
                new_argument = new_target - (new_offset + size)
                output[new_offset + 1:new_offset + 3] = struct.pack(
                    "<H",
                    new_argument,
                )
            elif opcode in absolute_jumps:
                old_target = int.from_bytes(
                    NEW_CODE[offset + 1:offset + 3],
                    "little",
                )
                output[new_offset + 1:new_offset + 3] = struct.pack(
                    "<H",
                    relocated(old_target),
                )

        offset += size

    return bytes(output)


FALLBACK_CODE = _build_fallback_code()


def _marshalled_code(code: bytes) -> bytes:
    return b"s" + struct.pack("<I", len(code)) + code


def patch(path: Path) -> bool:
    data = path.read_bytes()
    old_count = data.count(OLD_CODE)
    broken_count = data.count(BROKEN_CODE)
    new_count = data.count(NEW_CODE)
    fallback_count = data.count(FALLBACK_CODE)

    if (
        old_count == 0
        and broken_count == 0
        and new_count == 0
        and fallback_count == 1
    ):
        print(f"Already patched: {path}")
        return False
    if old_count + broken_count + new_count != 1 or fallback_count != 0:
        raise RuntimeError(
            "Unexpected Avatar.pyc layout: "
            f"old={old_count}, broken={broken_count}, "
            f"dynamic={new_count}, fallback={fallback_count}"
        )

    if old_count == 1:
        source = OLD_CODE
    elif broken_count == 1:
        source = BROKEN_CODE
    else:
        source = NEW_CODE

    patched = data.replace(
        _marshalled_code(source),
        _marshalled_code(FALLBACK_CODE),
        1,
    )

    if patched == data:
        raise RuntimeError(
            "Avatar.pyc function code was found without its marshal header"
        )

    path.write_bytes(patched)
    print(f"Patched character appearance: {path}")
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
        / "Avatar.pyc",
    )
    args = parser.parse_args()
    patch(args.path.resolve())


if __name__ == "__main__":
    main()
