import io
import hashlib
from platform import system
import tempfile
import unittest
from dateutil import tz
from components.img_generator import img_generator
from protos.planning_pb2 import Planning
from protos.activity_id_pb2 import ActivityID
from protos.activity_pb2 import Activity
from protos.rated_player_pb2 import RatedPlayer


class GeneratorTester(unittest.TestCase):
    """Test class for the image generator."""

    def test_planning(self):
        """
        Verifies the hash of generated GIFs to ensure the images stay the same.
        """
        p = Planning()
        a = p.activities.add()
        a.id.type = ActivityID.Type.LEVIATHAN
        a.id.when.datetime = '2020-07-14T23:55:00+02:00'
        a.id.when.time_specified = True
        a.state = Activity.State.NOT_STARTED
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        a = p.activities.add()
        a.id.type = ActivityID.Type.SPIRE_OF_STARS_PRESTIGE
        a.id.when.datetime = '2020-07-23'
        a.id.when.time_specified = False
        a.state = Activity.State.NOT_STARTED
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        a = p.activities.add()
        a.id.type = ActivityID.Type.SCOURGE_OF_THE_PAST
        a.id.when.datetime = '2020-10-25T16:30:00+01:00'
        a.id.when.time_specified = True
        a.state = Activity.State.MILESTONED
        a.milestone = "save au boss"
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.UNKNOWN
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        a = p.activities.add()
        a.id.type = ActivityID.Type.GARDEN_OF_SALVATION
        a.id.when.datetime = '2020-08-25T22:35:00+02:00'
        a.id.when.time_specified = True
        a.state = Activity.State.FINISHED
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        a = p.activities.add()
        a.id.type = ActivityID.Type.WRATH_OF_THE_MACHINE
        a.id.when.datetime = '2019-01-25T04:42:00+01:00'
        a.id.when.time_specified = True
        a.state = Activity.State.NOT_STARTED
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        a = p.activities.add()
        a.id.type = ActivityID.Type.LAST_WISH
        a.state = Activity.State.NOT_STARTED
        (a.squad.players.add()).gamer_tag = "snippro34"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Jezehbell"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Carnage"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.substitutes.add()).gamer_tag = "Oby1Chick"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER

        gen = img_generator.Generator(tz.gettz('Europe/Paris'), "fr")
        gifs = gen.generate_images(p)

        hash_reference = {
            "Darwin": [
                "6c3a69069413955d2007ebf10fee7d289769aedec2b015fa0b56e742735d4beb",
                "941aa1047be76e8e98ecfe7dff9ad6bd2083e5b2ca1c6d913bd3fd634a0b9e8d"
            ],
            "Linux": [
                "f23f0dd977779129253e1925e80c2b7eec2abc6013ff8f54448b9e91b0a0c3a1",
                "5f6f8181c66235040e946b7c16a7f8407cdc8d0c2b089095f5dfd3317e11f5ff"
            ]
        }

        detected_os = system()
        self.assertTrue(detected_os in hash_reference.keys(), "OS not supported to run tests")

        gif_hashes = []
        for gif in gifs:
            self.assertEqual(gif.tell(), 0)
            gif.seek(0, io.SEEK_END)
            self.assertLess(gif.tell(), 8*1024*1024)
            gif.seek(0, io.SEEK_SET)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as temp:
                temp.write(gif.getbuffer())
                print("NOTE - the result of this test can be visualized here: ", temp.name)
            gif_hashes.append(hashlib.sha256(gif.getbuffer()).hexdigest())
        self.assertEqual(gif_hashes, hash_reference[detected_os], True)


if __name__ == '__main__':
    unittest.main()
