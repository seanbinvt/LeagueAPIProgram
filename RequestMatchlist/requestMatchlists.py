import time
import json

# Library for ease of Riot Game API use.
# https://riot-watcher.readthedocs.io/en/latest/
from riotwatcher import RiotWatcher, ApiError

apiKey = json.load(open("keys.json", encoding="UTF-8"))['apiKey']

api = RiotWatcher(apiKey)

# -- For this file refer to MatchApiV4 in the Riot-Watcher source code --

""" Returns JSON object of information regarding the games played in the last 7 days. Maximum return of 100 games.

Keyword arguments:
region -- LoL region to use for search scope. 
summonerId -- ID of the player account to be searched.
"""


def requestLastWeek(region, summonerId):
    currentTime = round(time.time() * 1000)  # Current time in epoch MS
    response = api.match.matchlist_by_account(
        region, summonerId, 420, currentTime - (86400000 * 7))  # 4 is the ID for 5x5 RANKED SOLO QUEUE
    return response


""" Returns JSON object of information regarding the last (maximum) 100 games played.

Keyword arguments:
apiKey -- Dev unique Riot games API key.
region -- LoL region to use for search scope. 
summonerId -- ID of the player account to be searched.
"""


def requestLastGames(region, summonerId):
    response = api.match.matchlist_by_account(region, summonerId, 420)
    return(response)
