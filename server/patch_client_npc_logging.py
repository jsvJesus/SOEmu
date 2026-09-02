"""Add minimal NPC construction logging to the shipped Python 2.6 bytecode.

The client buffers python.log while it is running. Printing npcName from the
end of NPC.__init__ lets protocol work distinguish an entity that was never
constructed from one whose model or placement is wrong.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


OLD_CODE = bytes.fromhex(
    "7400006901007c0000830100017c00006902007403006904007403006905006702"
    "006a07006f1100017406006901007c0000830100016e0100017c00006907006401"
    "006a02006f1100017408006901007c0000830100016e0100017409006901007c00"
    "00830100016400007c00005f0b0064000053"
)

# print self.npcName; self.facingTracker1 = None; return None
NEW_CODE = OLD_CODE[:-13] + bytes.fromhex(
    "7c000069070047486400007c00005f0b0064000053"
)

OLD_ENTER_CODE = bytes.fromhex(
    "7400006901007c00007c0100830200017402006903008300007c00005f04007405"
    "006901007c0000830100017c00006906006f4000017402006907007c0000690800"
    "6401007c00006909008303007c00005f0a007402006907007c0000690800640200"
    "7c0000690b008303007c00005f0c006e010001740d00690e00690f007c00006910"
    "008301006400006a03006f380001740d00690e00690f007c000069100083010064"
    "03006a03006f1c0001740d00690e00690f007c00006910008301007c00005f1200"
    "6e01000164000053"
)

# Log only after Avatar.onEnterWorld and the model setup completed.
NEW_ENTER_CODE = OLD_ENTER_CODE[:-4] + bytes.fromhex(
    "7c0000691000474864000053"
)


def _marshalled_code(code: bytes) -> bytes:
    return b"s" + struct.pack("<I", len(code)) + code


def patch(path: Path) -> bool:
    data = path.read_bytes()
    old = _marshalled_code(OLD_CODE)
    new = _marshalled_code(NEW_CODE)
    old_enter = _marshalled_code(OLD_ENTER_CODE)
    new_enter = _marshalled_code(NEW_ENTER_CODE)
    old_count = data.count(old)
    new_count = data.count(new)
    old_enter_count = data.count(old_enter)
    new_enter_count = data.count(new_enter)

    if (
        old_count == 0
        and new_count == 1
        and old_enter_count == 0
        and new_enter_count == 1
    ):
        print(f"Already patched: {path}")
        return False
    if old_count + new_count != 1 or old_enter_count + new_enter_count != 1:
        raise RuntimeError(
            "Unexpected NPC.pyc layout: "
            f"init={old_count}/{new_count}, "
            f"enter={old_enter_count}/{new_enter_count}"
        )

    if old_count:
        data = data.replace(old, new, 1)
    if old_enter_count:
        data = data.replace(old_enter, new_enter, 1)
    path.write_bytes(data)
    print(f"Patched NPC construction logging: {path}")
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
        / "NPC.pyc",
    )
    args = parser.parse_args()
    patch(args.path.resolve())


if __name__ == "__main__":
    main()
