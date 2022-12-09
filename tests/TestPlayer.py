import unittest
import Player

data = {
    "name": "example username",
    "tag": "example tag",
    "currenttierpatched": "example tier",
    "images": {"small": "example image"},
    "ranking_in_tier": "S tier",
    "mmr_change_to_last_game": "99",
}

stats = [
    {
        "metadata": {"rounds_played": 2},
        "players": {
            "all_players": [
                {
                    "name": "example username",
                    "tag": "example tag",
                    "stats": {
                        "kills": 10,
                        "deaths": 2,
                        "score": 230,
                        "headshots": 10,
                        "bodyshots": 10,
                        "legshots": 10,
                    },
                },
                {
                    "name": "wrong username",
                    "tag": "wrong tag",
                    "stats": {
                        "kills": 200,
                        "deaths": 2,
                        "score": 300,
                        "headshots": 100,
                        "bodyshots": 10,
                        "legshots": 10,
                    },
                },
            ]
        },
    },
    {
        "metadata": {"rounds_played": 2},
        "players": {
            "all_players": [
                {
                    "name": "example username",
                    "tag": "example tag",
                    "stats": {
                        "kills": 20,
                        "deaths": 5,
                        "score": 280,
                        "headshots": 35,
                        "bodyshots": 51,
                        "legshots": 81,
                    },
                },
                {
                    "name": "wrong username",
                    "tag": "wrong tag",
                    "stats": {
                        "kills": 20,
                        "deaths": 22,
                        "score": 303,
                        "headshots": 10,
                        "bodyshots": 100,
                        "legshots": 10,
                    },
                },
            ]
        },
    },
]


class TestPlayer(unittest.TestCase):
    # Assure getUsername works
    def test_username(self):
        p = Player.Player(data)
        self.assertEqual(p.getUsername(), "example username")

    # Assure getTag works
    def test_tag(self):
        p = Player.Player(data)
        self.assertEqual(p.getTag(), "example tag")

    # Assure getRank works
    def test_rank(self):
        p = Player.Player(data)
        self.assertEqual(p.getRank(), "example tier")

    # Assure getImage works
    def test_image(self):
        p = Player.Player(data)
        self.assertEqual(p.getImage(), "example image")

    # Assure getRR works
    def test_rr(self):
        p = Player.Player(data)
        self.assertEqual(p.getRR(), "S tier")

    # Assure getRRChange works
    def test_rr_change(self):
        p = Player.Player(data)
        self.assertEqual(p.getRRChange(), "99")

    # Assure getKD works
    def test_kd(self):
        p = Player.Player(data)
        self.assertEqual(p.getKD(), 0.0)

    # Assure getACS works
    def test_acs(self):
        p = Player.Player(data)
        self.assertEqual(p.getACS(), 0.0)

    # Assure getHeadshot works
    def test_headshot(self):
        p = Player.Player(data)
        self.assertEqual(p.getHeadshot(), 0.0)

    # Assure parseStats works
    def test_parsestats(self):
        p = Player.Player(data)
        p.parseStats(stats)
        self.assertEqual(p.getKD(), 4.5)
        self.assertEqual(p.getACS(), 127.5)
        self.assertAlmostEqual(p.getHeadshot(), 22.84263959)
