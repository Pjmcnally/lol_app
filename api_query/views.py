from django.shortcuts import render, redirect
from django.contrib import messages
from api_query.models import Game

from secrets import API_KEY

import requests
from datetime import timedelta
from random import choice

base_url = 'https://na.api.pvp.net/'
region = 'na'
platform = 'NA1'
payload = {'api_key': API_KEY}


# Create your views here.
def home_page(request, error_msg=""):
    """ Renders home page with random featured game participant """
    featured_url = 'https://na.api.pvp.net/observer-mode/rest/featured'

    r = requests.get(featured_url, params=payload)

    player_list = []
    player = ""

    if r.status_code == 200:
        for game in r.json()['gameList']:
            for summ in game['participants']:
                player_list.append(summ['summonerName'])
            player = choice(player_list)
    else:
        messages.error(request, 'Featured game API is down at the moment.',
                                extra_tags='api_down')
    return render(request, 'home.html', {
        'player': player,
        })


def get_game(request):
    """ gets summoner ID and passes info to dashboard """
    if request.POST:
        sum_name = request.POST.get('summoner_name', '')
        sum_id = get_id(sum_name)

        if sum_id == "error":
            messages.error(request, 'That does not appear to be a valid\
                summoner name. Please try again', extra_tags='search')
            return redirect('/')
        else:
            return redirect('/dashboard?sum_id={sum_id}'.format(
                            sum_id=str(sum_id)))
    else:
        return redirect('/')


def get_id(sum_name):
    """ Makes API call to get player ID from summoner name and returns it """
    id_url = '{b}api/lol/{r}/v1.4/summoner/by-name/{n}'

    sum_name = sum_name.replace(" ", "")

    r = requests.get(id_url.format(b=base_url, r=region, n=sum_name),
                     params=payload)

    if r.status_code == 200:
        return r.json()[sum_name.lower()]['id']
    else:
        return "error"


def dashboard(request):
    """ renders dashboard """
    sum_id = request.GET.get('sum_id', '')

    game_url = '{b}observer-mode/rest/consumer/getSpectatorGameInfo/{p}/{s_id}'
    rank_url = '{b}api/lol/{r}/v2.5/league/by-summoner/{ids}/entry'

    r = requests.get(game_url.format(b=base_url, p=platform, s_id=sum_id),
                     params=payload)

    if r.status_code != 200:
        messages.error(request, 'That summoner is not currently playing a game.\
            Please try again', extra_tags='search')
        return redirect('/')
    else:
        game_info = r.json()

        p_id_list = [summ['summonerId'] for summ in game_info['participants']]
        r = requests.get(rank_url.format(b=base_url, r=region,
                         ids=", ".join(map(str, p_id_list))), params=payload)

        rank_info = r.json()

        this_game = Game(game_info, rank_info)

        print(this_game)

    return render(request, 'dashboard.html', {
        'id_searched': int(sum_id),
        'blue_team': [x for x in this_game.players if x.team == "blue"],
        'red_team': [x for x in this_game.players if x.team == "red"],
        'map': this_game.map,
        'mode': this_game.mode,
        'time': timedelta(seconds=this_game.length),
        'duration': this_game.length,
    })
