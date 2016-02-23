import json
import requests

from secrets import API_KEY

def list_check(stuff):
    if type(stuff) == list:
        return stuff.pop()
    else:
        return stuff


def get_champ_data():
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion"
    payload = {'api_key': API_KEY}

    r = requests.get(url, params=payload)
    data = r.json()
    version = data["version"]
    output = []

    for val in data["data"].values():
        champ = {}
        champ["pk"] = val["id"]
        champ["model"] = "api_query.ChampStatic"
        champ["fields"] = {}
        champ["fields"]["name"] = val["name"]
        champ["fields"]["descript"] = val["title"]
        champ["fields"]["image"] = val["key"]
        champ["fields"]["version"] = version
        output.append(champ)

    with open('champions_fix.json', "w") as f:
        json.dump(output, f, indent=2)


def get_mast_data():
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/mastery"
    payload = {'masteryListData':'all', 'api_key': API_KEY}

    r = requests.get(url, params=payload)
    data = r.json()
    version = data["version"]
    output = []

    for val in data["data"].values():
        mast = {}
        mast["pk"] = val["id"]
        mast["model"] = "api_query.MastStatic"
        mast["fields"] = {}
        mast["fields"]["name"] = val["name"]
        mast["fields"]["descript"] = list_check(val["sanitizedDescription"])
        mast["fields"]["tree"] = val["masteryTree"]
        mast["fields"]["ranks"] = val["ranks"]
        mast["fields"]["image"] = val["image"]["full"]
        mast["fields"]["version"] = version
        output.append(mast)

    with open('masteries_fix.json', "w") as f:
        json.dump(output, f, indent=2)


def get_rune_data():
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/rune"
    payload = {'runeListData':'all', 'api_key': API_KEY}

    r = requests.get(url, params=payload)
    data = r.json()
    version = data["version"]
    output = []

    for val in data["data"].values():
        rune = {}
        rune["pk"] = val["id"]
        rune["model"] = "api_query.RuneStatic"
        rune["fields"] = {}
        rune["fields"]["name"] = val["name"]
        rune["fields"]["descript"] = val["sanitizedDescription"]
        rune["fields"]["image"] = val["image"]["full"]
        rune["fields"]["version"] = version
        output.append(rune)

    with open('runes_fix.json', "w") as f:
        json.dump(output, f, indent=2)

def get_spell_data():
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/summoner-spell"
    payload = {'spellData':'all', 'api_key': API_KEY}

    r = requests.get(url, params=payload)
    data = r.json()
    version = data["version"]
    output = []

    for val in data["data"].values():
        spell = {}
        spell["pk"] = val["id"]
        spell["model"] = "api_query.SpellStatic"
        spell["fields"] = {}
        spell["fields"]["name"] = val["name"]
        spell["fields"]["descript"] = val["sanitizedDescription"]
        spell["fields"]["image"] = val["image"]["full"]
        spell["fields"]["version"] = version
        output.append(spell)

    with open('spells_fix.json', "w") as f:
        json.dump(output, f, indent=2)




if __name__ == '__main__':
    get_champ_data()
    get_mast_data()
    get_rune_data()
    get_spell_data()
