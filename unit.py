import unittest
import player

data = {"name" : "example username",
        "tag" : "example tag",
        "currenttierpatched" : "example tier",
        "images": {"small" : "example image"},
        "ranking_in_tier" : "S tier",
        "mmr_change_to_last_game" : "99"}

class TestPlayer(unittest.TestCase):
    def test_username(self):
        p = player.Player(data)
        self.assertEqual(p.getUsername(), "example username")
