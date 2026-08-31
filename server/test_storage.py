import time
import unittest

import storage


class StorageValueTests(unittest.TestCase):
    def test_identity_normalization_is_case_insensitive(self):
        self.assertEqual(
            storage.normalize_identity("  Stalker_1 "),
            storage.normalize_identity("stalker_1"),
        )

    def test_password_hash_is_salted_and_verifiable(self):
        salt_a, digest_a = storage._new_password_record("secret")
        salt_b, digest_b = storage._new_password_record("secret")

        self.assertNotEqual(salt_a, salt_b)
        self.assertNotEqual(digest_a, digest_b)
        self.assertTrue(storage._verify_password("secret", salt_a, digest_a))
        self.assertFalse(storage._verify_password("wrong", salt_a, digest_a))

    def test_character_deletion_remaining_time(self):
        character = storage.CharacterRecord(
            id=1,
            account_id=1,
            name="stalker",
            models_wire=b"\x00" * 60,
            player_kit_wire=storage.DEFAULT_PLAYER_KIT_WIRE,
            is_tutorial_passed=0,
            charstats_wire=storage.DEFAULT_CHARSTATS_WIRE,
            gold_credit=0,
            renames_available=0,
            rename_required=False,
            deletion_deadline=time.time() + 60,
            last_space="spaces/so_origins",
            position=(1.0, 2.0, 3.0),
            direction=(0.0, 0.0, 0.0),
        )

        self.assertGreater(character.deletion_remaining_time, 59.0)
        self.assertLessEqual(character.deletion_remaining_time, 60.0)


if __name__ == "__main__":
    unittest.main()
