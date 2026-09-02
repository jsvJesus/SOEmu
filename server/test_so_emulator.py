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

    def test_corrupted_saved_position_uses_world_spawn(self):
        session = make_session()
        character = make_character(
            is_tutorial_passed=1,
            last_space="spaces/city_lubech",
            position=(0.0, float("nan"), 1e30),
        )

        emu.configure_player_character(session, character, tutorial=1)

        self.assertEqual(session.play_geometry, b"spaces/city_lubech")
        self.assertEqual(
            session.play_position,
            emu.PLAYER_WORLD_LUBECH_POSITION,
        )


class PlayerWireTests(unittest.TestCase):
    def test_implicit_movement_uses_little_endian_coordinates(self):
        session = make_session()
        session.active_character_id = 1
        movement = bytes([emu.AVATAR_UPDATE_IMPLICIT_MESSAGE_ID]) + struct.pack(
            "<fffBBBB",
            37.25,
            4.75,
            63.5,
            27,
            24,
            0,
            55,
        )

        emu.describe_baseapp_messages(session, movement)

        self.assertEqual(session.play_position, (37.25, 4.75, 63.5))
        self.assertTrue(session.position_dirty)

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
        session.begin_play_name = "Admin"
        session.active_default_models_wire = emu.SAFE_DEFAULT_MODELS_WIRE

        message = emu.build_avatar_cell_player_message(session)

        self.assertEqual(message[0], 6)
        self.assertEqual(
            struct.unpack_from("<H", message, 1)[0],
            len(message) - 3,
        )
        self.assertGreater(len(message) - 3, 32)
        self.assertEqual(struct.unpack_from("<ii", message, 3), (1, 0))
        position = struct.unpack_from("<fff", message, 11)
        for actual, expected in zip(position, emu.PLAYER_WORLD_STATION_POSITION):
            self.assertAlmostEqual(actual, expected, places=5)

    def test_cell_player_contains_complete_initial_property_stream(self):
        session = make_session()
        emu.configure_player_world(session, tutorial=0)
        session.begin_play_name = "Admin"
        session.active_default_models_wire = struct.pack(
            "<15i",
            1, 2, 25,
            3, 4, 200008,
            5, 6, 200205,
            7, 8, 110248,
            9, 10, 200650,
        )
        session.active_gold_credit = 25

        message = emu.build_avatar_cell_player_message(session)
        expected_properties = emu.AVATAR_ENTITY_DEF.build_cell_player_stream(
            {
                "name": emu._pack_bigworld_string("Admin"),
                "defaultModels": session.active_default_models_wire,
                "GoldCreditNumber": struct.pack("<i", 25),
                "passTutorial": b"\x00",
            }
        )

        self.assertEqual(message[35:], expected_properties)
        self.assertGreater(len(expected_properties), 1000)
        self.assertIn(b"\x05Admin", expected_properties)
        self.assertIn(session.active_default_models_wire, expected_properties)

    def test_required_character_defaults_are_concrete(self):
        definition = emu.AVATAR_ENTITY_DEF

        def default_wire(name):
            prop = definition.properties[name]
            return definition._encode_value(
                prop.type_spec,
                prop.default_node,
            )

        self.assertEqual(default_wire("Stats"), b"\x05" * 6)
        self.assertEqual(default_wire("hungry"), struct.pack("<f", 1.0))
        self.assertEqual(default_wire("thirst"), struct.pack("<f", 1.0))

        for name in (
            "CarryingItems",
            "StoredItems",
            "quickSlotBar",
            "relationsWithFractions",
        ):
            self.assertEqual(default_wire(name), struct.pack("<i", 0))

    def test_default_models_zero_slots_use_original_client_fallbacks(self):
        models = struct.pack(
            "<15i",
            10, 11, 25,
            20, 21, 0,
            30, 31, 200205,
            40, 41, 0,
            50, 51, 200650,
        )

        normalised = struct.unpack(
            "<15i",
            emu.normalise_avatar_models_wire(models),
        )

        self.assertEqual(normalised[0:3], (10, 11, 25))
        self.assertEqual(normalised[3:6], (20, 21, 200010))
        self.assertEqual(normalised[6:9], (30, 31, 200205))
        self.assertEqual(normalised[9:12], (40, 41, 110247))
        self.assertEqual(normalised[12:15], (50, 51, 200650))

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

    def test_tutorial_npc_enter_uses_world_entity_id(self):
        npc = emu.TUTORIAL_NPCS[0]

        message = emu.build_tutorial_npc_enter_message(npc, 0)

        self.assertEqual(message[0], 0x0A)
        self.assertEqual(struct.unpack_from("<i", message, 1)[0], npc.entity_id)
        self.assertEqual(message[-1], 0)

    def test_tutorial_npcs_use_server_owned_entity_ids(self):
        # BigWorld reserves IDs >= (1 << 30) + 1 for client-only entities.
        # NPCs sent by the emulator must stay below that range.
        ids = [npc.entity_id for npc in emu.TUTORIAL_NPCS]
        first_client_id = (1 << 30) + 1

        self.assertTrue(all(3 < entity_id < first_client_id for entity_id in ids))
        self.assertEqual(len(ids), len(set(ids)))

    def test_tutorial_npc_create_uses_volatile_wire_format(self):
        npc = emu.TUTORIAL_NPCS[0]

        message = emu.build_tutorial_npc_create_message(npc)

        self.assertEqual(message[0], 0x08)
        self.assertEqual(struct.unpack_from("<H", message, 1)[0], len(message) - 3)
        self.assertEqual(message[3], 0)  # BW_COMPRESSION_NONE
        self.assertEqual(
            struct.unpack_from("<iH", message, 4),
            (npc.entity_id, emu.NPC_ENTITY_TYPE_ID),
        )
        for actual, expected in zip(
            struct.unpack_from("<fff", message, 10),
            npc.position,
        ):
            self.assertAlmostEqual(actual, expected, places=5)

        self.assertEqual(
            message[22:25],
            emu._pack_yaw_pitch_roll(npc.yaw, 0.0, 0.0),
        )

        property_stream = message[25:]
        self.assertEqual(property_stream[0], 17)
        self.assertEqual(
            property_stream[1],
            emu.NPC_ENTITY_DEF.client_property_index("npcType"),
        )
        self.assertIn(b"\x06Zevaka", property_stream)

    def test_tutorial_roster_matches_original_quest_holders(self):
        self.assertEqual(
            {npc.npc_name for npc in emu.TUTORIAL_NPCS},
            {
                "Zevaka",
                "Soldat_Noob",
                "Dejurnyi",
                "Trader_Noob",
                "Aid_trader_noob",
                "Repairman_Noob",
                "Ammo_trader_noob",
                "Armor_trader_noob",
                "Provodnik_Noob",
                "Haron_Corpse",
            },
        )

    def test_tutorial_npcs_face_their_reconstructed_landmarks(self):
        by_name = {npc.npc_name: npc for npc in emu.TUTORIAL_NPCS}

        self.assertTrue(
            all(npc.yaw != 0.0 for npc in emu.TUTORIAL_NPCS)
        )
        self.assertEqual(
            by_name["Soldat_Noob"].position,
            (-61.9033, -2.4801, 87.0193),
        )
        self.assertAlmostEqual(
            by_name["Armor_trader_noob"].yaw,
            2.896250,
        )
        self.assertAlmostEqual(
            by_name["Provodnik_Noob"].yaw,
            0.373340,
        )

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
