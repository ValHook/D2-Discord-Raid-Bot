from concurrent.futures import ThreadPoolExecutor
from functools import reduce
import itertools
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

MAX_NETWORK_WORKERS = 32
MAX_NETWORK_RETRIES_PER_REQUEST = 7
BACKOFF_FACTOR = 0.5
STATUS_FORCELIST = (500, 502, 504)
BUNGIE_API_ENDPOINT = 'https://www.bungie.net/platform'
DESTINY_2_CLANS_WATCHLIST = [ 
                              696852, # La fine equipe du 11
							  4220683, # Finis Terræ
                              379807, # Les Francs Gardiens
                              1890420, # Le Survivant du Cuirassé
                              1907122, # Olympic Gaming
                            ]
DESTINY_2_ACTIVITIES_BY_HASH = {
    1875726950: ActivityID.Type.CALUS,
    2693136600: ActivityID.Type.CALUS,
    2693136601: ActivityID.Type.CALUS,
    2693136602: ActivityID.Type.CALUS,
    2693136603: ActivityID.Type.CALUS,
    2693136604: ActivityID.Type.CALUS,
    2693136605: ActivityID.Type.CALUS,
    417231112: ActivityID.Type.CALUS_PRESTIGE,
    757116822: ActivityID.Type.CALUS_PRESTIGE,
    1685065161: ActivityID.Type.CALUS_PRESTIGE,
    3446541099: ActivityID.Type.CALUS_PRESTIGE,
    3879860661: ActivityID.Type.CALUS_PRESTIGE,
    2449714930: ActivityID.Type.CALUS_PRESTIGE,
    2164432138: ActivityID.Type.EATER_OF_WORLDS,
    3089205900: ActivityID.Type.EATER_OF_WORLDS,
    809170886: ActivityID.Type.EATER_OF_WORLDS_PRESTIGE,
    119944200: ActivityID.Type.SPIRE_OF_STARS,
    3213556450: ActivityID.Type.SPIRE_OF_STARS_PRESTIGE,
    3333172150: ActivityID.Type.CROWN_OF_SORROW,
    2122313384: ActivityID.Type.LAST_WISH,
    548750096: ActivityID.Type.SCOURGE_OF_THE_PAST,
    2812525063: ActivityID.Type.SCOURGE_OF_THE_PAST,
    2659723068: ActivityID.Type.GARDEN_OF_SALVATION,
}

class Fetcher:
    """Parser for user input (intents)."""

    def __init__(self, api_key):
        if not isinstance(api_key, str) or len(api_key) == 0:
            raise ValueError("Clé d'API Bungie non spécifiée")
        self.__api_key = api_key
        self.__executor = ThreadPoolExecutor(max_workers=MAX_NETWORK_WORKERS)

    def fetch(self):
        self.start_new_session()
        destiny2_data = self.fetch_destiny2_data()
        self.close_session()
        bundle = APIBundle()
        for row in destiny2_data:
            gamer_tag = row[0]
            stat = APIBundle.Stats.ActivityStat()
            stat.activity_type = row[1]
            stat.completions = row[2]
            bundle.stats_by_player[gamer_tag].activity_stats.append(stat)
        return bundle

    def fetch_destiny2_data(self): 
        players = self.parallel_flat_map(lambda clanID: self.fetch_destiny2_clan_members(clanID), DESTINY_2_CLANS_WATCHLIST)
        characters = self.parallel_flat_map(lambda player: self.fetch_destiny2_player_characters(player), players)
        completions = self.parallel_flat_map(lambda character: self.fetch_destiny2_character_activity_completions(character), characters)
        completions_by_player = self.reduce_by_key(lambda c: (c[2], c[4]), lambda c1, c2: (c1[0], c1[1], c1[2], c1[3]+","+c1[3], c1[4], c1[5]+c2[5]), completions)
        completions_by_player = map(lambda c: (c[0], c[4], c[5]), completions_by_player)
        return completions_by_player

    def fetch_destiny2_clan_members(self, clanID):
        response = self.request('/GroupV2/'+str(clanID)+'/members/').json()
        results = response['Response']['results']
        members = map(lambda result: result['destinyUserInfo'], results)
        members = map(lambda member: (member['displayName'], str(member['membershipType']), str(member['membershipId'])), members)
        return members

    def fetch_destiny2_player_characters(self, player):
        displayName = player[0]
        membershipType = player[1]
        membershipID = player[2]
        response = self.request('/Destiny2/'+membershipType+'/Profile/'+membershipID+'/?components=Characters').json()
        results = response['Response']['characters']['data'].keys()
        characters = map(lambda characterID: (displayName, membershipType, membershipID, str(characterID)), results)
        return characters

    def fetch_destiny2_character_activity_completions(self, character):
        displayName = character[0]
        membershipType = character[1]
        membershipID = character[2]
        characterID = character[3]
        defaults = []
        for activity_type in DESTINY_2_ACTIVITIES_BY_HASH.values():
            defaults.append((displayName, membershipType, membershipID, characterID, activity_type, 0))
        path = '/Destiny2/'+membershipType+'/Account/'+membershipID+'/Character/'+characterID+'/Stats/AggregateActivityStats/'
        response = self.request(path).json()
        try:
            results = response['Response']['activities']
        except:
            return defaults
        results = filter(lambda result: result['activityHash'] in DESTINY_2_ACTIVITIES_BY_HASH, results)
        results = map(lambda result: (DESTINY_2_ACTIVITIES_BY_HASH[result['activityHash']], int(result['values']['activityCompletions']['basic']['value'])), results)
        activities = map(lambda result: (displayName, membershipType, membershipID, characterID, result[0], result[1]), results)
        activities = list(activities) + defaults
        completions = self.reduce_by_key(lambda a: a[4], lambda a1, a2: (a1[0], a1[1], a1[2], a1[3], a1[4], a1[5]+a2[5]), activities)
        return completions
    
    def reduce_by_key(self, key_function, reduce_function, iterable):
        iterable = list(iterable)
        iterable.sort(key=key_function)
        grouped = [list(values) for key, values in itertools.groupby(iterable, key_function)]
        return map(lambda row: reduce(reduce_function, row), grouped)

    def parallel_map(self, function, iterable):
        return self.__executor.map(function, iterable)

    def parallel_flat_map(self, function, iterable):
        matrix = self.parallel_map(function, iterable)
        return itertools.chain(*matrix)

    def start_new_session(self):
        session = requests.Session()
        retry = Retry(
            total=MAX_NETWORK_RETRIES_PER_REQUEST,
            read=MAX_NETWORK_RETRIES_PER_REQUEST,
            connect=MAX_NETWORK_RETRIES_PER_REQUEST,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=STATUS_FORCELIST,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({'X-API-KEY': self.__api_key})
        self.__session = session

    def request(self, path):
        return self.__session.get(BUNGIE_API_ENDPOINT + path)

    def close_session(self):
        self.__session.close()
        self.__session = None