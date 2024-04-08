from helpers import get_account_info, get_summoner_info, get_match_ids_by_summoner_puuid, \
     did_player_win_match, win_percent_of_last_20_games
import settings

gameName= 'Randomdude02'
tagLine= 'NA1'

account = get_account_info(gameName, tagLine, region=settings.DEFAULT_REGION)

print("")
print(account)
print("")

encryptedPUUID = account['puuid']
tagLine = account['tagLine']

summoner = get_summoner_info(encryptedPUUID, tagLine)

print("")
print(summoner)
print("")

summoner_match_ids = get_match_ids_by_summoner_puuid(summoner['puuid'], 20)
print(summoner_match_ids)
print("")

win = did_player_win_match(summoner['puuid'], summoner_match_ids[0])
print(win)
print("")

win_ratio = win_percent_of_last_20_games(gameName)
print(win_ratio)