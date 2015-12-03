from django.shortcuts import render
from django.http import HttpResponse

import requests


# Create your views here.
def home_page(request):
    if request.method=='POST':
        full_url = 'https://na.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}'
        region = 'na'
        payload = {'api_key': 'c57f551f-be34-4afc-829c-bd45dc4123c8'}

        sum_name = request.POST.get('summoner_name', '')

        full_url = full_url.replace('{region}', region)
        full_url = full_url.replace('{summonerNames}', sum_name)

        r = requests.get(full_url, params=payload)

        stuff = r.json()
        sum_id = stuff[sum_name.lower()]['id']

        return render(request, 'home.html', {
            'sum_name': sum_name,
            'sum_id': sum_id,
            })
    else:
        return render(request, 'home.html')

# r = requests.get(full_url, params=payload)
# print(r.status_code)
# # print(r.text)
# # print(r.json)
# stuff = r.json()

# for x in stuff.items():
#     print("")
#     print(x)
# print("")
