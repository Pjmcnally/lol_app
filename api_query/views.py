from django.shortcuts import render, redirect
from api_query.models import ChampStatic, SpellStatic, MastStatic, RuneStatic

from secrets import API_KEY

import requests
from random import choice

pre_url = 'https://na.api.pvp.net/'
payload = {'api_key': API_KEY}


# Create your views here.
def home_page(request, error_msg=""):
    """ Renders home page with random featured game participant """
    featured_url = 'https://na.api.pvp.net/observer-mode/rest/featured'

    r = requests.get(featured_url, params=payload)

    player_list = []

    if r.status_code == 200:
        # name variable
        for x in r.json()['gameList']:
            for y in x['participants']:
                player_list.append(y['summonerName'])

        return render(request, 'home.html', {
            'player': choice(player_list),
            'error_msg': error_msg,
            })
    else:
        return render(request, 'home.html', {
            'player': "Featured game API is not working",
            'error_msg': error_msg,
            })


def get_game(request):
    """ gets summoner ID and passes info to dashboard """
    if request.POST:
        sum_name = request.POST.get('summoner_name', '')
        sum_id = get_id(sum_name)

        if sum_id == "error":
            # Find out how to enter error message here
            return redirect('/')
        else:
            return redirect('/dashboard?sum_id={sum_id}'.format(
                            sum_id=str(sum_id)))
    else:
        return redirect('/')


def get_id(sum_name):
    """ Makes API call to get player ID from summoner name and returns it """
    name_to_id_url = 'api/lol/{region}/v1.4/summoner/by-name/{summonerNames}'
    region = 'na'

    sum_name = sum_name.replace(" ", "")

    full_url = pre_url + name_to_id_url

    full_url = full_url.replace('{region}', region)
    full_url = full_url.replace('{summonerNames}', sum_name)

    r = requests.get(full_url, params=payload)

    if r.status_code == 200:
        return r.json()[sum_name.lower()]['id']
    else:
        return "error"

def dashboard(request):
    """ renders dashboard """
    sum_id = request.GET.get('sum_id', '')

    game_url = '/observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}'
    platform = 'NA1'

    full_url = pre_url + game_url

    # switch to format (not replace)
    full_url = full_url.replace('{platformId}', platform)
    full_url = full_url.replace('{summonerId}', sum_id)

    r = requests.get(full_url, params=payload)

    if r.status_code != 200:
        # Find out how to enter error message here
        return redirect('/')
    else:
        info = r.json()

        this_game = Game(info)

        # Test Area begins
        test_player_json = {'profileIconId': 982, 'teamId': 100, 'runes': [{'count': 9, 'runeId': 5273}, {'count': 9, 'runeId': 5290}, {'count': 9, 'runeId': 5316}, {'count': 1, 'runeId': 5365}, {'count': 2, 'runeId': 8022}], 'summonerId': 24137629, 'spell1Id': 4, 'championId': 27, 'bot': False, 'summonerName': 'Doublestop', 'masteries': [{'rank': 5, 'masteryId': 6114}, {'rank': 1, 'masteryId': 6122}, {'rank': 5, 'masteryId': 6134}, {'rank': 1, 'masteryId': 6142}, {'rank': 5, 'masteryId': 6211}, {'rank': 1, 'masteryId': 6223}, {'rank': 5, 'masteryId': 6232}, {'rank': 1, 'masteryId': 6242}, {'rank': 5, 'masteryId': 6251}, {'rank': 1, 'masteryId': 6263}], 'spell2Id': 12}
        test_player = Player(test_player_json)

        print(test_player)



        # Test area ends

        for summ in info['participants']:
            print(summ)
            summ['champName'] = ChampStatic.objects.get(id=summ['championId']).name
            summ['champImage'] = ChampStatic.objects.get(id=summ['championId']).image
            summ['champTitle'] = ChampStatic.objects.get(id=summ['championId']).descript
            summ['spell1Image'] = SpellStatic.objects.get(id=summ['spell1Id']).image
            summ['spell1Name'] = SpellStatic.objects.get(id=summ['spell1Id']).name
            summ['spell1Descript'] = SpellStatic.objects.get(id=summ['spell1Id']).descript
            summ['spell2Image'] = SpellStatic.objects.get(id=summ['spell2Id']).image
            summ['spell2Name'] = SpellStatic.objects.get(id=summ['spell2Id']).name
            summ['spell2Descript'] = SpellStatic.objects.get(id=summ['spell2Id']).descript

            ferocity, cunning, resolve = 0, 0, 0
            for mast in summ['masteries']:
                if MastStatic.objects.get(id=mast['masteryId']).tree == "Ferocity":
                    ferocity += mast['rank']
                if MastStatic.objects.get(id=mast['masteryId']).tree == "Cunning":
                    cunning += mast['rank']
                if MastStatic.objects.get(id=mast['masteryId']).tree == "Resolve":
                    resolve += mast['rank']

            summ['masteryTotal'] = str(ferocity) + "/" + str(cunning) +"/" + str(resolve)

            for rune in summ['runes']:
                rune['image'] = RuneStatic.objects.get(id=rune['runeId']).image
                rune['descript'] = RuneStatic.objects.get(id=rune['runeId']).descript
                rune['name'] = RuneStatic.objects.get(id=rune['runeId']).name

    return render(request, 'dashboard.html', {
        'blue_team': [x for x in info['participants'] if x["teamId"]==100],
        'red_team': [x for x in info['participants'] if x["teamId"]==200],
        'map': this_game.map,
        'mode': this_game.mode,
    })



class Game():
    def __init__(self, game_json):
        self.length = game_json['gameLength']
        self.id = game_json['gameId']
        self.start_time = game_json['gameStartTime']
        self.mode = self.mode_name(game_json['gameQueueConfigId'])
        self.map = self.map_name(game_json['mapId'])
        self.blue_bans = []
        self.red_bans = []
        self.blue_team = []
        self.red_team = []


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
                     41: "ARAM"}
        return mode_dict[info]

    def map_name(self, info):
        """ converts map id into human readable string """
        map_dict = {10: "Twisted Treeline", 11: "Summoner's Rift",
                    12: "Howling Abyss"}
        return map_dict[info]

class Player():
    def __init__(self, summ):
        self.name = summ["summonerName"]
        self.champion = Champion(summ['championId'])

    def __str__(self):
        return "{} is playing {}".format(self.name, self.champion.name)

class Champion():
    dd_link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/champion/{n}.png"

    def __init__(self, champ_id):
        self.name = ChampStatic.objects.get(id=champ_id).name
        self.descript = ChampStatic.objects.get(id=champ_id).descript
        self.image = ChampStatic.objects.get(id=champ_id).image
        self.version = ChampStatic.objects.get(id=champ_id).version
        self.image_link = self.dd_link.format(v = self.version, n = self.image)

    def __str__(self):
        return "Name = {}\nImage = {}\nDescript = {}\n{}".format(self.name, self.image, self.descript, self.image_link)

class Spell():
    dd_link = "https://ddragon.leagueoflegends.com/cdn/{v}/img/spell/{n}"
