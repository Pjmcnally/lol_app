import json
import requests

url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/mastery?api_key=c57f551f-be34-4afc-829c-bd45dc4123c8"

r = requests.get(url)

output = []

for x in data["data"]:
    champ = {}
    champ["pk"] = data["data"][x]["id"]
    champ["model"] = "api_query.champion"
    champ["fields"] = {}
    champ["fields"]["name"] = data["data"][x]["name"]
    champ["fields"]["title"] = data["data"][x]["title"]
    champ["fields"]["key"] = data["data"][x]["key"]
    output.append(champ)

# output = str(output)
# output.replace("'", '"')

with open('champions_fix.json', "w") as f:
    json.dump(output, f)