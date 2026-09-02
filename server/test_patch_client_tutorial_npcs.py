import subprocess
import tempfile
import unittest
from pathlib import Path

from xdis.bytecode import Bytecode
from xdis.load import load_module
from xdis.op_imports import get_opcode_module

import patch_client_tutorial_npcs as patcher


ROOT = Path(__file__).resolve().parents[1]
class TutorialNPCClientPatchTests(unittest.TestCase):
    def test_patch_adds_grounded_tutorial_roster_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "PlayerAvatar.pyc"
            target.write_bytes(
                subprocess.check_output(
                    [
                        "git",
                        "show",
                        "HEAD:packs/res/scripts/client/PlayerAvatar.pyc",
                    ],
                    cwd=ROOT,
                )
            )

            first_result = patcher.patch(target)
            second_result = patcher.patch(target)

            method = patcher._find_method(load_module(str(target))[3], "onGeometryMapped")
            instructions = list(
                Bytecode(method, get_opcode_module((2, 6)))
            )
            create_index = method.co_names.index("createEntity")
            collide_index = method.co_names.index("collide")

            self.assertIn(patcher.MARKER, method.co_consts)
            self.assertEqual(
                sum(
                    instruction.opname == "LOAD_ATTR"
                    and instruction.arg == create_index
                    for instruction in instructions
                ),
                len(patcher.TUTORIAL_NPCS),
            )
            self.assertEqual(
                sum(
                    instruction.opname == "JUMP_IF_TRUE"
                    for instruction in instructions
                ),
                len(patcher.TUTORIAL_NPCS),
            )
            self.assertEqual(
                sum(
                    instruction.opname == "LOAD_ATTR"
                    and instruction.arg == collide_index
                    for instruction in instructions
                ),
                len(patcher.TUTORIAL_NPCS),
            )
            self.assertEqual(len(patcher.TUTORIAL_NPCS), 10)
            self.assertNotIn("Eger", {npc[0] for npc in patcher.TUTORIAL_NPCS})
            self.assertTrue(
                all(yaw != 0.0 for name, _position, yaw, _props
                    in patcher.TUTORIAL_NPCS if name != "Haron_Corpse")
            )
            soldier = next(
                npc for npc in patcher.TUTORIAL_NPCS
                if npc[0] == "Soldat_Noob"
            )
            self.assertEqual(soldier[1], (-61.9033, -2.4801, 87.0193))
            self.assertTrue(first_result)
            self.assertFalse(second_result)


if __name__ == "__main__":
    unittest.main()
