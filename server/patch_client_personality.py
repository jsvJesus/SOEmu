"""Make the online client personality expose an empty player-data mapping.

The modified client Avatar.prerequisites() calls
BWPersonality.game.playersdata.get(...). Online startup leaves playersdata as
None, so initialise it as an empty dict. Offline startup may still replace it
with the contents of playersdata.json.
"""

from __future__ import annotations

import argparse
from pathlib import Path


OLD_CODE = bytes.fromhex(
    "7409007c00005f15006400007c00005f160064000053"
)
# Early local version used Python 2.7's opcode number for BUILD_MAP. Python
# 2.6 uses 0x68; recognise 0x69 so an already modified client self-repairs.
BROKEN_CODE = bytes.fromhex(
    "7409007c00005f15006900007c00005f160064000053"
)
NEW_CODE = bytes.fromhex(
    "7409007c00005f15006800007c00005f160064000053"
)


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
            "Unexpected BWPersonality.pyc layout: "
            f"old={old_count}, broken={broken_count}, new={new_count}"
        )

    source = OLD_CODE if old_count == 1 else BROKEN_CODE
    path.write_bytes(data.replace(source, NEW_CODE, 1))
    print(f"Patched online playersdata initialisation: {path}")
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
        / "BWPersonality.pyc",
    )
    args = parser.parse_args()
    patch(args.path.resolve())


if __name__ == "__main__":
    main()
