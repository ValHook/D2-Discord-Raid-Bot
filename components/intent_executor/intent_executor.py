from datetime import datetime
from datetime import tzinfo
from dateutil import tz
import dateparser
from components.api_fetcher.api_fetcher import Fetcher
from components.converters.when import to_datetime
from components.img_generator.img_generator import Generator
from components.storage.storage import Storage
from protos.activity_pb2 import Activity
from protos.intent_pb2 import Intent
from protos.planning_pb2 import Planning

CLEARPAST_WEEKDAY = "Tuesday"
CLEARPAST_HOUR = 19
TIMEZONE = tz.gettz('Europe/Paris')
MAX_SQUAD_SIZE_PLAYERS = 6
MIN_SQUAD_SIZE_PLAYERS = 1
MAX_SQUAD_SIZE_SUBSTITUTES = 2
MIN_SQUAD_SIZE_SUBSTITUTES = 0


class Executor:
    """Executor for user input (intents)."""

    def __init__(self, storage, api_fetcher, img_generator):
        assert isinstance(storage, Storage), "Stockage non configuré"
        assert isinstance(api_fetcher, Fetcher), "Connexion API non configurée"
        assert isinstance(img_generator, Generator), "Générateur d'images non configuré"
        self.__storage = storage
        self.__api_fetcher = api_fetcher
        self.__img_generator = img_generator

    def execute(self, intent, now):
        """
        :param intent: The intent to execute
        :param now: Now as a datetime.
        :return: An (execution feedback message, generated BytesIO images or None) tuple.
        :raises: If the intent could be executed for some reason.
        """
        assert isinstance(intent, Intent), "Commande invalide"
        assert isinstance(now, datetime), "Horloge non configurée"
        assert isinstance(now.tzinfo, tzinfo), "Fuseau horaire non configuré"
        if intent.HasField('global_intent'):
            return self.execute_global_intent(intent.global_intent, now)
        if intent.HasField('activity_intent'):
            return self.execute_activity_intent(intent.activity_intent), None
        raise ValueError("Commande invalide")

    def execute_global_intent(self, global_intent, now):
        """
        :param global_intent: The global_intent to execute.
        :param now: Now as a datetime.
        :return: An (execution feedback message, generated BytesIO images or None) tuple.
        :raises: If the intent could be executed for some reason.
        """
        if global_intent.HasField('generate_images'):
            # !raid images
            planning = self.__storage.read_planning()
            images = self.__img_generator.generate_images(planning)
            if len(images) == 0:
                return "Il n'y a aucune activité dans le planning pour le moment.", []
            return "Affiches pour les activités en cours:", images

        if global_intent.HasField('sync_bundle'):
            # !raid sync
            bundle = self.__api_fetcher.fetch(now)
            self.__storage.write_api_bundle(bundle)
            return "Joueurs et niveaux d'experiences synchronisés.", None

        if global_intent.HasField('get_last_bundle_sync_datetime'):
            # !raid lastsync
            bundle = self.__storage.read_api_bundle()
            return "Dernière synchronisation: " + bundle.last_sync_datetime, None

        if global_intent.HasField('clear_all'):
            # !raid clearall
            planning = Planning()
            self.__storage.write_planning(planning)
            return "Toutes les activités du planning sont désormais supprimées.", None

        if global_intent.HasField('clear_past'):
            # !raid clearpast
            planning = self.__storage.read_planning()
            threshold = dateparser.parse(
                CLEARPAST_WEEKDAY,
                settings={'PREFER_DATES_FROM': 'past', 'RELATIVE_BASE': now}
            )
            threshold = threshold.replace(hour=CLEARPAST_HOUR)
            threshold = threshold.replace(tzinfo=TIMEZONE)
            activities = filter(
                lambda a: not a.id.when or threshold <= to_datetime(a.id.when, now.tzinfo),
                planning.activities
            )
            planning = Planning()
            planning.activities.extend(activities)
            self.__storage.write_planning(planning)
            feedback = "Les activités des semaines précédentes ont été suprimées.\n"
            feedback += "Les activités restantes dans le planning sont:\n"
            feedback += str(planning)
            return feedback, None

        raise ValueError("Commande invalide")

    def execute_activity_intent(self, activity_intent):
        """
        :param activity_intent: The global_intent to execute.
        :return: An execution feedback message tuple.
        :raises: If the intent could be executed for some reason.
        """
        planning = self.__storage.read_planning()
        activity_id = activity_intent.activity_id
        if activity_intent.HasField('update_when'):
            # !raid date
            activity = self.find_activity_with_id(activity_id, planning)
            activity.id.when.CopyFrom(activity_intent.update_when)
            self.__storage.write_planning(planning)
            return "Date mise à jour:\n" + str(activity.id)

        if activity_intent.HasField('mark_finished'):
            # !raid finish [activity] (date)
            activity = self.find_activity_with_id(activity_id, planning)
            activity.state = Activity.State.FINISHED
            self.__storage.write_planning(planning)
            return "Good job!\nActivité marquée comme terminée:\n" + str(activity.id)

        if activity_intent.HasField('set_milestone'):
            # !raid milestone [activity] (date)
            activity = self.find_activity_with_id(activity_id, planning)
            activity.state = Activity.State.MILESTONED
            activity.milestone = activity_intent.set_milestone
            self.__storage.write_planning(planning)
            return "Étape mise à jour (" + activity.milestone + "):\n" + str(activity.id)

        if activity_intent.HasField('clear'):
            # !raid clear [activity] (date)
            activity = self.find_activity_with_id(activity_id, planning)
            planning.activities.remove(activity)
            self.__storage.write_planning(planning)
            return "Activité supprimée:\n" + str(activity.id)

        if activity_intent.HasField('upsert_squad'):
            # !raid (backup) [activity] (date) [players]
            feedback = "Escouade mise à jour"
            try:
                activity = self.find_activity_with_id(activity_id, planning)
            except:
                activity = planning.activities.add()
                activity.id.CopyFrom(activity_intent.activity_id)
                activity.state = Activity.State.NOT_STARTED
                feedback = "Activité créée"
            self.merge_players(
                activity.squad.players,
                activity_intent.upsert_squad.added.players,
                False
            )
            self.merge_players(
                activity.squad.players,
                activity_intent.upsert_squad.removed.players,
                True
            )
            self.merge_players(
                activity.squad.substitutes,
                activity_intent.upsert_squad.added.substitutes,
                False
            )
            self.merge_players(
                activity.squad.substitutes,
                activity_intent.upsert_squad.removed.substitutes,
                True
            )
            self.assert_player_count_within_bound(
                activity.squad.players,
                MIN_SQUAD_SIZE_PLAYERS,
                MAX_SQUAD_SIZE_PLAYERS
            )
            self.assert_player_count_within_bound(
                activity.squad.substitutes,
                MIN_SQUAD_SIZE_SUBSTITUTES,
                MAX_SQUAD_SIZE_SUBSTITUTES
            )
            self.__storage.write_planning(planning)
            return feedback + ":\n" + str(activity)

        raise ValueError("Commande invalide")

    def find_activity_with_id(self, activity_id, planning):
        """
        Finds the activity that best matches the given ID.
        :param activity_id: The activity ID used for the search.
        It can be incomplete (i.e without the When)
        :param planning: The planning to search from.
        :return: The desired match.
        :raises: If there are 0 or more than 1 matches.
        """
        activities = planning.activities
        activity_type = activity_id.type
        date_time = to_datetime(activity_id.when, TIMEZONE)
        date = date_time.date() if date_time else None
        search_by_type = date_time is None
        search_by_date = not search_by_type and not activity_id.when.time_specified
        search_by_datetime = not search_by_type and not search_by_date

        # Search by type.
        if search_by_type:
            activities = filter(lambda a: a.id.type == activity_type, planning.activities)

        # Search by date.
        elif search_by_date and date:
            activities = map(lambda a: (a, to_datetime(a.id.when, TIMEZONE)), activities)
            activities = filter(
                lambda a: a[1] and a[1].date() == date,
                activities
            )
            activities = map(lambda a: a[0], activities)

        # Search by datetime.
        elif search_by_datetime and date_time:
            activities = filter(
                lambda a: a.id.when == activity_id.when,
                activities
            )

        activities = list(activities)
        if len(activities) == 0:
            raise ValueError("Aucune activité trouvée pour:\n" + str(activity_id))
        if len(activities) == 1:
            return activities[0]
        raise ValueError("Critère de recherche trop large. Précisez une date et une heure.")

    def merge_players(self, base, delta, subtract):
        """
        :param base: The array of players the delta must be merged into.
        :param delta: The players to merge into the base.
        :param subtract: Whether the delta is positive or negative.
        """
        result = []
        if subtract:
            delta_gamer_tags = set(map(lambda p: p.gamer_tag, delta))
            result = list(filter(lambda p: p.gamer_tag not in delta_gamer_tags, base))
            del base[:]
            base.extend(result)
        else:
            base_gamer_tags = set(map(lambda p: p.gamer_tag, base))
            players_to_add = list(filter(lambda p: p.gamer_tag not in base_gamer_tags, delta))
            players_to_edit = dict()
            for player in delta:
                if player.gamer_tag in base_gamer_tags:
                    players_to_edit[player.gamer_tag] = player
            for player in base:
                if player.gamer_tag in players_to_edit:
                    player.rating = players_to_edit[player.gamer_tag].rating
            base.extend(players_to_add)

    def assert_player_count_within_bound(self, players, min_capacity, max_capacity):
        """
        :param min_capacity: Minimum expected size. Inclusive.
        :param max_capacity: Maximum expected size. Inclusive.
        :raises: if len(players) is not within the bounds.
        """
        count = len(players)
        if count < min_capacity:
            raise ValueError(
                "Il n'y a pas assez de joueurs %d/%d." % (count, min_capacity)
            )
        if count > max_capacity:
            raise ValueError(
                "Il y a trop de joueurs %d/%d." % (count, max_capacity)
            )
