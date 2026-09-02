import tempfile
import unittest
from pathlib import Path

import patch_client_npc_logging as patcher


class NPCLoggingPatchTests(unittest.TestCase):
    def test_patch_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "NPC.pyc"
            path.write_bytes(
                b"prefix"
                + patcher._marshalled_code(patcher.OLD_CODE)
                + patcher._marshalled_code(patcher.OLD_ENTER_CODE)
                + b"suffix"
            )

            self.assertTrue(patcher.patch(path))
            self.assertFalse(patcher.patch(path))
            self.assertIn(
                patcher._marshalled_code(patcher.NEW_CODE),
                path.read_bytes(),
            )
            self.assertIn(
                patcher._marshalled_code(patcher.NEW_ENTER_CODE),
                path.read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
