import struct
import unittest

import so_emulator as emu
import storage


def make_session(world_mode="auto"):
    return emu.Session(
        username="test",
        account_id=1,
        blowfish_key=b"test-key",
        login_session_key=1,
        login_client_addr=("127.0.0.1", 10000),
        created_at=0.0,
        world_mode=world_mode,
    )


class TutorialRoutingTests(unittest.TestCase):
    def test_auto_routes_new_character_to_station(self):
        session = make_session()
        emu.configure_player_world(session, tutorial=0)

        self.assertEqual(session.play_geometry, b"spaces/so_origins")
        self.assertEqual(session.play_position, emu.PLAYER_WORLD_STATION_POSITION)
        self.assertEqual(session.play_pass_tutorial, 0)

    def test_auto_routes_passed_tutorial_to_lubech(self):
        session = make_session()
        emu.configure_player_world(session, tutorial=1)

        self.assertEqual(session.play_geometry, b"spaces/city_lubech")
        self.assertEqual(session.play_position, emu.PLAYER_WORLD_LUBECH_POSITION)
        self.assertEqual(session.play_pass_tutorial, 1)

    def test_lubech_override_is_safe_fallback(self):
        session = make_session("lubech")
        emu.configure_player_world(session, tutorial=0)

        self.assertEqual(session.play_geometry, b"spaces/city_lubech")
        self.assertEqual(session.play_pass_tutorial, 1)

    def test_passed_character_resumes_saved_lubech_position(self):
        session = make_session()
        character = make_character(
            is_tutorial_passed=1,
            last_space="spaces/city_lubech",
            position=(10.0, 20.0, 30.0),
        )

        emu.configure_player_character(session, character, tutorial=1)

        self.assertEqual(session.play_geometry, b"spaces/city_lubech")
        self.assertEqual(session.play_position, (10.0, 20.0, 30.0))


class PlayerWireTests(unittest.TestCase):
    def test_default_models_property_uses_persisted_wire(self):
        session = make_session()
        session.active_default_models_wire = bytes(range(60))

        message = emu.build_player_default_models_message(session)

        # FD: generic property entity message; body is EntityID, the path for
        # Avatar.defaultModels index 117, then the exact 60-byte packed model.
        self.assertEqual(message[:9].hex(), "fd4200030000003a80")
        self.assertEqual(message[9:], bytes(range(60)))

    def test_default_models_rejects_truncated_database_value(self):
        session = make_session()
        session.active_default_models_wire = b"short"

        with self.assertRaises(ValueError):
            emu.build_player_default_models_message(session)

    def test_pass_tutorial_high_property_wire(self):
        session = make_session()
        emu.configure_player_world(session, tutorial=0)

        message = emu.build_player_pass_tutorial_message(session)

        # FD: property entity message; 07 00: uint16 body length; EntityID=3;
        # 1f 00: stop bit + 8-bit property index 62; final 00: INT8 value.
        self.assertEqual(message.hex(), "fd0700030000001f0000")

    def test_cell_player_uses_saved_station_start_position(self):
        session = make_session()
        emu.configure_player_world(session, tutorial=0)

        message = emu.build_avatar_cell_player_message(session)

        self.assertEqual(message[0], 6)
        self.assertEqual(struct.unpack_from("<H", message, 1)[0], 32)
        self.assertEqual(struct.unpack_from("<ii", message, 3), (1, 0))
        position = struct.unpack_from("<fff", message, 11)
        for actual, expected in zip(position, emu.PLAYER_WORLD_STATION_POSITION):
            self.assertAlmostEqual(actual, expected, places=5)

    def test_space_data_contains_selected_geometry(self):
        station = make_session()
        emu.configure_player_world(station, tutorial=0)
        station_message = emu.build_player_space_data_message(station)

        lubech = make_session()
        emu.configure_player_world(lubech, tutorial=1)
        lubech_message = emu.build_player_space_data_message(lubech)

        self.assertTrue(station_message.endswith(b"spaces/so_origins"))
        self.assertTrue(lubech_message.endswith(b"spaces/city_lubech"))
        self.assertEqual(struct.unpack_from("<H", station_message, 1)[0], 95)
        self.assertEqual(struct.unpack_from("<H", lubech_message, 1)[0], 96)

    def test_character_list_serializes_persisted_character(self):
        session = make_session()
        character = make_character(is_tutorial_passed=1, gold_credit=25)

        message = emu.build_character_list_message(session, [character])

        self.assertEqual(message[0], 0x8E)
        self.assertEqual(struct.unpack_from("<i", message, 7)[0], 1)
        self.assertIn(b"stalker", message)
        self.assertEqual(
            struct.unpack_from("<H", message, 1)[0],
            len(message) - 3,
        )


class CharacterValidationTests(unittest.TestCase):
    def test_shipped_russian_name_rules(self):
        self.assertEqual(emu.validate_avatar_name("stalker_1"), ("stalker_1", 0))
        self.assertEqual(emu.validate_avatar_name("сталкер_1"), ("сталкер_1", 0))
        self.assertEqual(emu.validate_avatar_name("stалкер")[1], 3)
        self.assertEqual(emu.validate_avatar_name("_stalker")[1], 7)
        self.assertEqual(emu.validate_avatar_name("a")[1], 4)


def make_character(**changes):
    values = dict(
        id=1,
        account_id=1,
        name="stalker",
        models_wire=b"\x01" * 60,
        player_kit_wire=storage.DEFAULT_PLAYER_KIT_WIRE,
        is_tutorial_passed=0,
        charstats_wire=storage.DEFAULT_CHARSTATS_WIRE,
        gold_credit=0,
        renames_available=0,
        rename_required=False,
        deletion_deadline=None,
        last_space="spaces/so_origins",
        position=emu.PLAYER_WORLD_STATION_POSITION,
        direction=(0.0, 0.0, 0.0),
    )
    values.update(changes)
    return storage.CharacterRecord(**values)


if __name__ == "__main__":
    unittest.main()
