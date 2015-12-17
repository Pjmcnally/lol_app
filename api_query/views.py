from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from api_query.models import Champion, Spell, Mastery, Rune

from secrets import API_KEY

import requests
from random import choice

pre_url = 'https://na.api.pvp.net/'
payload = {'api_key': API_KEY}

# Create your views here.
def home_page(request, error_msg=""):  
    featured_url = 'https://na.api.pvp.net/observer-mode/rest/featured'

    r = requests.get(featured_url, params=payload)

    stuff = r.json()

    player_list = []

    for x in stuff['gameList']:
        for y in x['participants']:
            player_list.append(y['summonerName'])

    return render(request, 'home.html', {
        'player': choice(player_list),
        'error_msg': error_msg,
        })
    

def get_game(request):
    if request.POST:
        sum_name = request.POST.get('summoner_name', '')
        sum_id = get_id(sum_name)

        if sum_id == "error":
            # Find out how to enter error message here
            return redirect('/')
        else:
            return redirect('/dashboard?sum_id={sum_id}'.format(sum_id=str(sum_id)))
    else:
        return redirect('/')


def get_id(sum_name):
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
    sum_id = request.GET.get('sum_id', '')

    game_url = '/observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}'
    platform = 'NA1'
    summonerId = sum_id

    full_url = pre_url + game_url

    full_url = full_url.replace('{platformId}', platform)
    full_url = full_url.replace('{summonerId}', sum_id)

    r = requests.get(full_url, params=payload)

    if r.status_code != 200:
        # Find out how to enter error message here
        return redirect('/')
    else:
        stuff = r.json()

        # test = Champion.objects.get(id=36)
        # print(test.name)

        for summ in stuff['participants']:
            summ['champName'] = Champion.objects.get(id=summ['championId']).name
            summ['champImage'] = Champion.objects.get(id=summ['championId']).image
            summ['champTitle'] = Champion.objects.get(id=summ['championId']).descript
            summ['spell1Image'] = Spell.objects.get(id=summ['spell1Id']).image
            summ['spell1Name'] = Spell.objects.get(id=summ['spell1Id']).name
            summ['spell1Descript'] = Spell.objects.get(id=summ['spell1Id']).descript
            summ['spell2Image'] = Spell.objects.get(id=summ['spell2Id']).image
            summ['spell2Name'] = Spell.objects.get(id=summ['spell2Id']).name
            summ['spell2Descript'] = Spell.objects.get(id=summ['spell2Id']).descript
            
            ferocity, cunning, resolve = 0, 0, 0
            for mast in summ['masteries']:
                if Mastery.objects.get(id=mast['masteryId']).tree == "Ferocity":
                    ferocity += mast['rank']
                if Mastery.objects.get(id=mast['masteryId']).tree == "Cunning":
                    cunning += mast['rank']
                if Mastery.objects.get(id=mast['masteryId']).tree == "Resolve":
                    resolve += mast['rank']

            summ['masteryTotal'] = str(ferocity) + "/" + str(cunning) +"/" + str(resolve)

            for rune in summ['runes']:
                rune['image'] = Rune.objects.get(id=rune['runeId']).image
                rune['descript'] = Rune.objects.get(id=rune['runeId']).descript
                rune['name'] = Rune.objects.get(id=rune['runeId']).name



        blue = [x for x in stuff['participants'] if x["teamId"]==100]
        red = [x for x in stuff['participants'] if x["teamId"]==200]

        map_name = ""
        if stuff['mapId'] == 10:
            map_name = "Twisted Treeline"
        elif stuff['mapId'] == 11:
            map_name = "Summoner's Rift"
        elif stuff['mapId'] == 12:
            map_name = "Howling Abyss"

        mode_name = ""
        if stuff['gameQueueConfigId'] == 2:
            mode_name = "Normal 5v5 (Blind Pick)"
        elif stuff['gameQueueConfigId'] == 4:
            mode_name = "Ranked 5v5 (Solo Queue)"
        elif stuff['gameQueueConfigId'] == 8:
            mode_name = "Normal 3v3 (Draft Pick)"
        elif stuff['gameQueueConfigId'] == 14:
            mode_name = "Normal 5v5 (Draft Pick)"
        elif stuff['gameQueueConfigId'] == 41:
            mode_name = "Ranked Team 3v3"
        elif stuff['gameQueueConfigId'] == 42:
            mode_name = "Ranked Team 5v5"
        elif stuff['gameQueueConfigId'] == 61:
            mode_name = "Team Builder Game"
        elif stuff['gameQueueConfigId'] == 41:
            mode_name = "ARAM"





        return render(request, 'dashboard.html', {
            'sum_id': sum_id,
            'blue_team': blue,
            'red_team': red,
            'map': map_name,
            'mode': mode_name,
        })


