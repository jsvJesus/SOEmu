"""Patch the 0.6.5.3 client so persisted character appearance is respected.

The shipped Python 2.6 bytecode reads PACKED_AVATAR_MODEL.type_id and then
discards it in favour of hard-coded clothes/head defaults.  This is a
same-size bytecode patch, so the rest of Avatar.pyc and its marshal layout are
left untouched.
"""

from __future__ import annotations

import argparse
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


def patch(path: Path) -> bool:
    data = path.read_bytes()
    old_count = data.count(OLD_CODE)
    broken_count = data.count(BROKEN_CODE)
    new_count = data.count(NEW_CODE)

    if old_count == 0 and broken_count == 0 and new_count == 1:
        print(f"Already patched: {path}")
        return False
    if old_count + broken_count != 1 or new_count != 0:
        raise RuntimeError(
            "Unexpected Avatar.pyc layout: "
            f"old={old_count}, broken={broken_count}, new={new_count}"
        )

    source = OLD_CODE if old_count == 1 else BROKEN_CODE
    patched = data.replace(source, NEW_CODE, 1)
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
