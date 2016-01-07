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


def mode_name_func(info):
    """ converts mode id into human readable string """
    mode_dict = {2: "Normal 5v5 (Blind Pick)",
                 4: "Ranked 5v5 (Solo Queue)",
                 8: "Normal 3v3 (Draft Pick)",
                 14: "Normal 5v5 (Draft Pick)",
                 41: "Ranked Team 3v3",
                 42: "Ranked Team 5v5",
                 61: "Team Builder Game",
                 41: "ARAM"}
    return mode_dict[info.get('gameQueueConfigId', '')]


def map_name_func(info):
    """ converts map id into human readable string """
    map_dict = {10: "Twisted Treeline", 11: "Summoner's Rift",
                12: "Howling Abyss"}
    return map_dict[info.get('mapId', '')]


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

        print(info)

        for summ in info['participants']:
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
        'map': map_name_func(info),
        'mode': mode_name_func(info),
    })


class Game():
    def __init__(self, game_json):
        self.game_length = game_json[gameLength]

class Player():
    pass

class Champs():
    pass

class map():
    pass


