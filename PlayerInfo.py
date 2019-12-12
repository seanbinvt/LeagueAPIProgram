import json
# Library for ease of Riot Game API use.
# https://riot-watcher.readthedocs.io/en/latest/
from riotwatcher import RiotWatcher, ApiError
import RequestMatchlist.requestMatchlists as RequestMatchlists
# print(json.load(open("keys.json", encoding="UTF-8"))['apiKey'])
api = RiotWatcher(
    json.load(open("keys.json", encoding="UTF-8"))['apiKey'])

'''
PlayerInfo object defines all the information that makes up a summoner information
search window.

Error Handling:
if error == 'init' then either the league API is down, the API key is out of date, or the player name doesn't exist
if wins == 'none then there was no information in last week search
'''


class PlayerInfo():

    # Iterates through JSON return of API request to return JSON object of current season RANKED SOLO 5x5 information.
    def summonerSearch(self, id, region):
        stats = api.league.by_summoner(region, id)
        for stat in stats:
            if stat['queueType'] == "RANKED_SOLO_5x5":
                return stat

    # Iterates though a game and searches for the JSON array with the given player name to retrieve information.
    def gameWinLoss(self, game):
        for player in game['participantIdentities']:
            if player['player']['summonerName'].lower() == "mccloudi":
                return game['participants'][player['participantId'] - 1]['stats']['win']

    def __init__(self, name, region):
        self.name = name

        # Variable to define possible errors
        self.error = None

        # If the api request is successful then continue
        # if not then stop and change error var
        try:
            summoner = api.summoner.by_name(region, name)
        except:
            self.error = "init"
        # If no error then use api response to retireve needed information
        if not self.error == 'init':
            stats = self.summonerSearch(summoner['id'], region)

            self.rank = stats['tier'] + " " + stats['rank']  # Rank label
            self.rankedWins = stats['wins']  # Ranked Season Wins label
            self.rankedLosses = stats['losses']  # Ranked Season Losses label

            self.wins = 0
            self.losses = 0
            # Array positions represent lanes: 0=TOP, 1=JUNGLE, 2=MIDDLE, 3=CARRY, 4=SUPPORT
            self.laneWins = [0, 0, 0, 0, 0]
            self.laneLoss = [0, 0, 0, 0, 0]

            # adds champion KEY for every game for later use to find most player champion
            champPlayed = []

            # try to make api request for last 7 days information
            # if error then change error var
            try:
                matches = RequestMatchlists.requestLastWeek(
                    "na1", summoner['accountId'])

                # Iterate through every match in the returned matchlist from API
                #
                for match in matches['matches']:
                    champPlayed.append(match['champion'])

                    # Use game IDs in previous API response to directly access specific game information
                    game = api.match.by_id("na1", match['gameId'])
                    # Readjust lane/wins/losses based API response vars
                    if match['lane'] == 'TOP':
                        if self.gameWinLoss(game) == True:
                            self.laneWins[0] += 1
                            self.wins += 1
                        else:
                            self.laneLoss[0] += 1
                            self.losses += 1
                    elif match['lane'] == 'JUNGLE':
                        if self.gameWinLoss(game) == True:
                            self.laneWins[1] += 1
                            self.wins += 1
                        else:
                            self.laneLoss[1] += 1
                            self.losses += 1
                    elif match['lane'] == 'MID':
                        if self.gameWinLoss(game) == True:
                            self.laneWins[2] += 1
                            self.wins += 1
                        else:
                            self.laneLoss[2] += 1
                            self.losses += 1
                    elif match['lane'] == 'BOTTOM' and match['role'] == 'DUO_CARRY':
                        if self.gameWinLoss(game) == True:
                            self.laneWins[3] += 1
                            self.wins += 1
                        else:
                            self.laneLoss[3] += 1
                            self.losses += 1
                    elif match['lane'] == 'BOTTOM' and match['role'] == 'DUO_SUPPORT':
                        if self.gameWinLoss(game) == True:
                            self.laneWins[4] += 1
                            self.wins += 1
                        else:
                            self.laneLoss[4] += 1
                            self.losses += 1

                # Code used to get the most common champion
                # if tie then return either or
                self.res = max(set(champPlayed), key=champPlayed.count)
            # if error occurred in past 7 day API calls then change error var
            except:
                self.error = "none"
