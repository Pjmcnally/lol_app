from django.db import models
from abc import ABCMeta, abstractmethod

# Create your models here.
class ChampStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class MastStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    tree = models.CharField(max_length=500, default='')
    ranks = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class RuneStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class SpellStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')


class Game():
    def __init__(self, game_json, rank_json):
        self.length = game_json['gameLength']
        self.id = game_json['gameId']
        self.start_time = game_json['gameStartTime']
        self.mode = self.mode_name(game_json['gameQueueConfigId'])
        self.map = self.map_name(game_json['mapId'])
        self.bans = [] # place holder for future feature. 
        self.players = [Player(summ, rank_json) for summ in game_json['participants']]

    def __str__(self):
        return "Game length = {}\nGame Id = {}\nGame start time = {}\n{}\n{}".format(
            self.length, self.id, self.start_time, self.mode, self.map)

    def mode_name(self, info):
        """ converts mode id into human readable string """
        mode_dict = {2: "Normal 5v5 (Blind Pick)",
                     4: "Ranked 5v5 (Solo Queue)",
                     8: "Normal 3v3 (Draft Pick)",
                     14: "Normal 5v5 (Draft Pick)",
                     41: "Ranked Team 3v3",
                     42: "Ranked Team 5v5",
                     61: "Team Builder Game",
                     65: "ARAM"}
        return mode_dict[info]

    def map_name(self, info):
        """ converts map id into human readable string """
        map_dict = {10: "Twisted Treeline", 11: "Summoner's Rift",
                    12: "Howling Abyss"}
        return map_dict[info]
        

class Player():
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
        return "{n} is playing {c}\nhe is on {t} team".format(n=self.name, c=self.champion.name, t=self.team)

    def find_keystone(self, raw_mast):
        for mast in raw_mast:
            if 6160 <= mast['masteryId'] <= 6169 or 6260 <= mast['masteryId'] <= 6269 or 6360 <= mast['masteryId'] <= 6369:
                return Mastery(mast['masteryId'], mast['rank'])
        return None

    def parse_rank_info(self, s_id, rank_info):
        if str(s_id) in rank_info:
            for x in rank_info[str(s_id)]:
                if x["queue"] == "RANKED_SOLO_5x5":
                    league = x["tier"]
                    division = x["entries"][0]['division']
                    return Rank(league, division)
        return None

    def masteries_func(self, raw_mast):
        masteries = {'ferocity': 0, 'cunning': 0, 'resolve': 0}
        for mast in raw_mast:
            if MastStatic.objects.get(id=mast['masteryId']).tree == "Ferocity":
                masteries['ferocity'] += mast['rank']
            elif MastStatic.objects.get(id=mast['masteryId']).tree == "Cunning":
                masteries['cunning'] += mast['rank']
            elif MastStatic.objects.get(id=mast['masteryId']).tree == "Resolve":
                masteries['resolve'] += mast['rank']
        return "{f}/{c}/{r}".format(f=masteries['ferocity'], c=masteries['cunning'], r=masteries['resolve'])

    def runes_func(self, raw_runes):
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
    """ Docstring goes here """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/champion/{n}.png"
    db_location = ChampStatic

    def asset_type(self):
        return 'Champion'


class Spell(Asset):
    """ Docstring goes here """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/spell/{n}"
    db_location = SpellStatic

    def asset_type(self):
        return 'Spell'


class Rune(Asset):
    """ Docstring goes here """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/rune/{n}"
    db_location = RuneStatic

    def asset_type(self):
        return 'Rune'


class Mastery(Asset):
    """ Docstring goes here """

    link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/mastery/{n}"
    db_location = MastStatic

    def asset_type(self):
        return 'Mastery'


class Rank(object):
    """ Docstring goes here """

    link = "/static/icons/{n}"

    def __init__(self, league, tier):
        self.name = "{} {}".format(league.capitalize(), tier)
        self.descript = "" # Placeholder
        self.image = "{}_{}.png".format(league.lower(), tier.lower())
        self.image_link = self.link.format(n=self.image)
