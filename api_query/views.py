from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests

pre_url = 'https://na.api.pvp.net/'
payload = {'api_key': 'c57f551f-be34-4afc-829c-bd45dc4123c8'}

# Create your views here.
def home_page(request):    
    return render(request, 'home.html')

def get_game(request):
    if request.method=='POST':
        sum_name = request.POST.get('summoner_name', '')
        sum_id = get_id(sum_name)

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

    return r.json()[sum_name.lower()]['id']


def dashboard(request):
    sum_id = request.GET.get('sum_id', '')

    game_url = '/observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}'
    platform = 'NA1'
    summonerId = sum_id

    full_url = pre_url + game_url

    full_url = full_url.replace('{platformId}', platform)
    full_url = full_url.replace('{summonerId}', sum_id)

    r = requests.get(full_url, params=payload)
    stuff = r.json()


    blue = [x["summonerName"] for x in stuff['participants'] if x["teamId"]==100]
    red = [x["summonerName"] for x in stuff['participants'] if x["teamId"]==200]

    return render(request, 'dashboard.html', {
        'sum_id': sum_id,
        'blue_team': blue,
        'red_team': red,
    })


