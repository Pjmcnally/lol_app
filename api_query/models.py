from django.db import models
from abc import ABCMeta, abstractmethod


class ChampStatic(models.Model):
    """ Class to store Riot static champion data in database"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')


class MastStatic(models.Model):
    """ Class to store Riot static mastery data in database"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    tree = models.CharField(max_length=500, default='')
    ranks = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')


class RuneStatic(models.Model):
    """ Class to store Riot static rune data in database"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')


class SpellStatic(models.Model):
    """ Class to store Riot static summoner spell data in database"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')


class Game():
    """ Class to store and process all game data

    Game class takes in a Current Game JSON object and a rank JSON object
    both of which are requested from Riots API.
    """
    def __init__(self, game_json, rank_json):
        self.startTime = game_json['gameStartTime']
        self.length = game_json['gameLength']
        self.id = game_json['gameId']
        self.start_time = game_json['gameStartTime']
        self.mode = self.mode_name(game_json['gameQueueConfigId'])
        self.map = self.map_name(game_json['mapId'])
        self.bans = []  # place holder for future feature.
        self.players = [Player(summ, rank_json) for summ in game_json['participants']]

    def __str__(self):
        return "Game length = {}\nGame Id = {}\nGame start time = {}\
                \n{}\n{}".format(self.startTime, self.length, self.id,
                                 self.start_time, self.mode, self.map)

    def mode_name(self, info):
        """ converts mode id into human readable string """
        mode_dict = {
            0: "Custom game",
            2: "Normal 5v5 (Blind Pick)",
            4: "Ranked 5v5 (Solo Queue)",
            6: "Ranked 5v5 (Premade)",
            7: "Coop vs AI",
            8: "Normal 3v3 (Draft Pick)",
            9: "Ranked 3v3 (Premade)",
            14: "Normal 5v5 (Draft Pick)",
            16: "Dominion 5v5 (Blind Pick)",
            17: "Dominion 5v5 (Draft Pick)",
            25: "Dominion Coop vs AI",
            31: "Coop vs AI (Intro Bots)",
            32: "Coop vs AI (Beginner Bots)",
            33: "Coop vs AI (Intermediate Bots)",
            41: "Ranked Team 3v3",
            42: "Ranked Team 5v5",
            52: "Coop vs AI",
            61: "Team Builder Game",
            65: "ARAM",
            70: "One for All",
            72: "Snowdown 1v1",
            73: "Snowdown 2v2",
            75: "Hexakill (6v6)",
            76: "Ultra Rapid Fire",
            83: "Ultra Rapid Fire (Bots)",
            91: "Doom Bots Rank 1",
            92: "Doom Bots Rank 2",
            93: "Doom Bots Rank 5",
            96: "Ascension",
            98: "Hexakill",
            100: "Butcher's Bridge",
            300: "Poro King",
            310: "Nemesis",
            313: "Black Market Brawlers",
            400: "Normal 5v5 (Draft Pick)",
            410: "Ranked 5v5 (Draft Pick)"
        }
        return mode_dict[info]

    def map_name(self, info):
        """ converts map id into human readable string """
        map_dict = {10: "Twisted Treeline", 11: "Summoner's Rift",
                    12: "Howling Abyss"}
        return map_dict[info]


class Player():
    """ Class to store and process player data

    Player class takes in a portion of Current Game JSON object and a rank JSON object
    both of which are requested from Riots API.
    """
    def __init__(self, summ, rank_info):
        self.id = summ['summonerId']
        self.name = summ['summonerName']
        self.team = self.team_func(summ['teamId'])
        self.champion = Champion(summ['championId'])
        self.spell1 = Spell(summ['spell1Id'])
        self.spell2 = Spell(summ['spell2Id'])
        self.runes = self.runes_func(summ['runes'])
        self.masteries = self.masteries_func(summ['masteries'])
        self.keystone = self.find_keystone(summ['masteries'])
        self.rank = self.parse_rank_info(self.id, rank_info)

    def __str__(self):
        return "{n} is playing {c}\n on {t} team".format(n=self.name,
                                                         c=self.champion.name,
                                                         t=self.team)

    def find_keystone(self, raw_mast):
        """ Identifies and returns keystone masteries 

        The numbers below are magic numbers they are the range in which
        keystone masteries occur.
        """
        for mast in raw_mast:
            if 6160 <= mast['masteryId'] <= 6169 or\
               6260 <= mast['masteryId'] <= 6269 or\
               6360 <= mast['masteryId'] <= 6369:
                return Mastery(mast['masteryId'], mast['rank'])
        return None

    def parse_rank_info(self, s_id, rank_info):
        """ Parses player and rank info and returns Rank object

        Takes in a player ID and rank JSON object and indetifies the rank of 
        the player with the given ID and returns that as a rank object.

        If the player is not ranked None is returned. 
        """
        if str(s_id) in rank_info:
            for x in rank_info[str(s_id)]:
                if x["queue"] == "RANKED_SOLO_5x5":
                    league = x["tier"]
                    division = x["entries"][0]['division']
                    return Rank(league, division)
        return None

    def masteries_func(self, raw_mast):
        """ Counts and returns the number of each mastery per type """
        masteries = {'ferocity': 0, 'cunning': 0, 'resolve': 0}
        for mast in raw_mast:
            if MastStatic.objects.get(id=mast['masteryId']).tree == "Ferocity":
                masteries['ferocity'] += mast['rank']
            elif MastStatic.objects.get(id=mast['masteryId']).tree == "Cunning":
                masteries['cunning'] += mast['rank']
            elif MastStatic.objects.get(id=mast['masteryId']).tree == "Resolve":
                masteries['resolve'] += mast['rank']
        return "{f}/{c}/{r}".format(f=masteries['ferocity'],
                                    c=masteries['cunning'],
                                    r=masteries['resolve'])

    def runes_func(self, raw_runes):
        """ Takes in runes as part of a JSON object and returns a list of Rune 
        objects
        """

        runes = []
        for rune in raw_runes:
            runes.append(Rune(rune["runeId"], rune["count"]))
        return runes

    def team_func(self, team):
        if team == 100:
            return "blue"
        elif team == 200:
            return "red"


class Asset(object):
    """A base asset class for all Riot game assets"""

    __metaclass__ = ABCMeta

    link = None
    db_location = None

    def __init__(self, asset_id, num=1):
        self.name = self.db_location.objects.get(id=asset_id).name
        self.descript = self.db_location.objects.get(id=asset_id).descript
        self.image = self.db_location.objects.get(id=asset_id).image
        self.version = self.db_location.objects.get(id=asset_id).version
        self.image_link = self.link.format(v=self.version, n=self.image)
        self.num = num

    def __str__(self):
        return "{n}: {d}".format(n=self.name, d=self.descript)

    @abstractmethod
    def asset_type():
        """"Return a string representing the type of asset this is."""
        pass


class Champion(Asset):
    """ Champion asset class """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/champion/{n}.png"
    db_location = ChampStatic

    def asset_type(self):
        return 'Champion'


class Spell(Asset):
    """ Spell asset class """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/spell/{n}"
    db_location = SpellStatic

    def asset_type(self):
        return 'Spell'


class Rune(Asset):
    """ Rune  asset class """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/rune/{n}"
    db_location = RuneStatic

    def asset_type(self):
        return 'Rune'


class Mastery(Asset):
    """ Mastery asset class """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/mastery/{n}"
    db_location = MastStatic

    def asset_type(self):
        return 'Mastery'


class Rank(object):
    """ Rank asset class """

    link = "/static/icons/{n}"

    def __init__(self, league, tier):
        self.name = "{} {}".format(league.capitalize(), tier)
        self.descript = ""  # Placeholder
        self.image = "{}_{}.png".format(league.lower(), tier.lower())
        self.image_link = self.link.format(n=self.image)
