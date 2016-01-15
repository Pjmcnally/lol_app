from django.db import models

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


class Champion():
    dd_link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/champion/{n}.png"

    def __init__(self, champ_id):
        self.name = ChampStatic.objects.get(id=champ_id).name
        self.descript = ChampStatic.objects.get(id=champ_id).descript
        self.image = ChampStatic.objects.get(id=champ_id).image
        self.version = ChampStatic.objects.get(id=champ_id).version
        self.image_link = self.dd_link.format(v=self.version, n=self.image)

    def __str__(self):
        return "Name = {}\nImage = {}\nDescript = {}\n{}".format(self.name, self.image, self.descript, self.image_link)


class Spell():
    dd_link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/spell/{n}"

    def __init__(self, spell_id):
        self.name = SpellStatic.objects.get(id=spell_id).name
        self.descript = SpellStatic.objects.get(id=spell_id).descript
        self.image = SpellStatic.objects.get(id=spell_id).image
        self.version = SpellStatic.objects.get(id=spell_id).version
        self.image_link = self.dd_link.format(v=self.version, n=self.image)

    def __str__(self):
        return "{n} : {d}".format(n=self.name, d=self.descript)

class Rune():
    dd_link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/rune/{n}"

    def __init__(self, rune_id, count):
        self.name = RuneStatic.objects.get(id=rune_id).name
        self.descript = RuneStatic.objects.get(id=rune_id).descript
        self.image = RuneStatic.objects.get(id=rune_id).image
        self.version = RuneStatic.objects.get(id=rune_id).version
        self.image_link = self.dd_link.format(v=self.version, n=self.image)
        self.count = count

class Mastery():
    dd_link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/mastery/{n}"

    def __init__(self, mast_id, rank):
        self.name = MastStatic.objects.get(id=mast_id).name
        self.descript = MastStatic.objects.get(id=mast_id).descript
        self.image = MastStatic.objects.get(id=mast_id).image
        self.version = MastStatic.objects.get(id=mast_id).version
        self.image_link = self.dd_link.format(v=self.version, n=self.image)
        self.rank = rank

class Rank():
    local_link = "/static/icons/{n}"

    def __init__(self, league, tier):
        self.name = "{} {}".format(league.capitalize(), tier)
        self.descript = "" # Placeholder
        self.link = "{}_{}.png".format(league.lower(), tier.lower())
        self.image_link = self.local_link.format(n=self.link)
