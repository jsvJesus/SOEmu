import tempfile
import unittest
from pathlib import Path

import patch_client_personality as personality_patch


class ClientPersonalityPatchTests(unittest.TestCase):
    def test_python_26_build_map_opcode_is_used(self):
        self.assertIn(b"\x68\x00\x00", personality_patch.NEW_CODE)
        self.assertNotIn(b"\x69\x00\x00", personality_patch.NEW_CODE)

    def test_patch_is_present_and_idempotent(self):
        source_path = (
            Path(__file__).resolve().parents[1]
            / "packs"
            / "res"
            / "scripts"
            / "client"
            / "BWPersonality.pyc"
        )
        source = source_path.read_bytes()

        self.assertEqual(source.count(personality_patch.NEW_CODE), 1)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "BWPersonality.pyc"
            path.write_bytes(
                source.replace(
                    personality_patch.NEW_CODE,
                    personality_patch.OLD_CODE,
                    1,
                )
            )

            self.assertTrue(personality_patch.patch(path))
            self.assertEqual(
                path.read_bytes().count(personality_patch.NEW_CODE),
                1,
            )
            self.assertFalse(personality_patch.patch(path))


if __name__ == "__main__":
    unittest.main()
