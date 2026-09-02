import tempfile
import unittest
from pathlib import Path

import patch_avatar_appearance as appearance_patch


class AvatarAppearancePatchTests(unittest.TestCase):
    def test_dynamic_type_id_patch_is_upgraded_and_idempotent(self):
        source_path = (
            Path(__file__).resolve().parents[1]
            / "packs"
            / "res"
            / "scripts"
            / "client"
            / "Avatar.pyc"
        )
        source = source_path.read_bytes()
        fallback = appearance_patch._marshalled_code(
            appearance_patch.FALLBACK_CODE
        )
        dynamic = appearance_patch._marshalled_code(
            appearance_patch.NEW_CODE
        )

        self.assertEqual(source.count(fallback), 1)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Avatar.pyc"
            path.write_bytes(source.replace(fallback, dynamic, 1))

            self.assertTrue(appearance_patch.patch(path))
            self.assertEqual(path.read_bytes().count(fallback), 1)
            self.assertFalse(appearance_patch.patch(path))


if __name__ == "__main__":
    unittest.main()
