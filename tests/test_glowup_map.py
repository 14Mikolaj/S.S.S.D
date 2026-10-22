"""The illustrated map must show real travel keys without wrapping or clipping."""

import unittest

from sssd.content import LOCATIONS
from sssd.world_map import SHORT_NAMES, render_world_map


class WorldMapTests(unittest.TestCase):
    def choices(self, location):
        return {destination: str(index) for index, destination in
                enumerate(LOCATIONS[location]["neighbors"], 1)}

    def test_every_current_location_and_neighbor_key_are_inside_their_region(self):
        for current in LOCATIONS:
            choices = self.choices(current)
            for width in (48, 60, 75, 76, 78, 100, 200):
                with self.subTest(current=current, width=width):
                    drawing = render_world_map(current, choices, width)
                    self.assertIn(SHORT_NAMES[current] + "[@]", drawing)
                    for destination, key in choices.items():
                        self.assertIn(SHORT_NAMES[destination] + f"[{key}]", drawing)
                    for location in LOCATIONS:
                        self.assertEqual(1, drawing.count(SHORT_NAMES[location] + "["))
                    self.assertLessEqual(max(map(len, drawing.splitlines())), width)
                    self.assertLessEqual(len(drawing.splitlines()), 18 if width < 76 else 14)
                    self.assertTrue(drawing.isascii())

    def test_marker_numbers_are_supplied_not_global_location_numbers(self):
        drawing = render_world_map("farm", {"village": "7", "plains": "9"}, 78)
        self.assertIn("VILLAGE[7]", drawing)
        self.assertIn("PLAINS[9]", drawing)
        self.assertNotIn("VILLAGE[1]", drawing)

    def test_castle_shows_lock_without_hiding_actionable_key(self):
        drawing = render_world_map("bridge", self.choices("bridge"), 78)
        self.assertIn("CASTLE[3]", drawing)
        self.assertIn("LOCK", drawing)
        self.assertIn("CASTLE[#]", render_world_map("farm", self.choices("farm"), 48))
        opened = render_world_map("farm", self.choices("farm"), 48, sealed=True)
        self.assertIn("CASTLE[.]", opened)
        self.assertNotIn("LOCK", opened)

    def test_distant_destinations_have_no_actionable_number(self):
        drawing = render_world_map("village", self.choices("village"), 78)
        self.assertIn("CAVES[.]", drawing)
        self.assertIn("SEA[.]", drawing)
        self.assertIn("MOUNTAINS[.]", drawing)

    def test_narrow_terminals_get_no_partial_drawing(self):
        for width in (0, 20, 40, 47):
            self.assertEqual("", render_world_map("village", self.choices("village"), width))

    def test_impossible_routes_and_invalid_keys_are_rejected(self):
        invalid = ({"castle": "1"}, {"farm": "12"}, {"farm": 1},
                   {"farm": "1", "desert": "1"}, {"farm": "\x1b"})
        for choices in invalid:
            with self.subTest(choices=choices), self.assertRaises(ValueError):
                render_world_map("village", choices, 78)


if __name__ == "__main__":
    unittest.main()
