from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from api_query.models import Champion

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

        for x in stuff['participants']:
            x['champName'] = Champion.objects.get(id=x['championId']).name
            x['champImage'] = Champion.objects.get(id=x['championId']).image
            x['champTitle'] = Champion.objects.get(id=x['championId']).descript

        blue = [x for x in stuff['participants'] if x["teamId"]==100]
        red = [x for x in stuff['participants'] if x["teamId"]==200]




        return render(request, 'dashboard.html', {
            'sum_id': sum_id,
            'blue_team': blue,
            'red_team': red,
        })


