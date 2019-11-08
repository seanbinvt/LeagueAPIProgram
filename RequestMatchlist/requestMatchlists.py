import time
import json

apiKey = json.load(open("keys.json", encoding="UTF-8"))['apiKey']
print(apiKey)

""" Returns JSON object of information regarding the games played in the last 2 days.

Keyword arguments:
apiKey -- Dev unique Riot games API key.
region -- LoL region to use for search scope.
summonerId -- ID of the player account to be searched.

"""


def requestLastDay(apiKey, region, summonerId):
    currentTime = round(time.time() * 1000)  # Current time in UNIX time (MS)
    response = requests.get(
        "https://"+region+".api.riotgames.com/lol/match/v4/matchlists/by-account/"+summonerId+"?api_key="+apiKey)
    print(response.json())
    return response.json()
