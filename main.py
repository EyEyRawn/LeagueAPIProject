API_KEY = "RGAPI-92535861-2693-4b2c-ac04-cf11c5d1b74d"
DEFAULT_REGION = 'americas'
DEFAULT_TAG_LINE = 'NA1'

def get_account_info(gameName=None, tagLine=None, region=DEFAULT_REGION):
    
    """
    Wrapper for ACCOUNT-V1 API Portal
    Gets account information by using their Riot ID
    :return: Account information as a dictionary or None if there's an issue
    """
    
    if not (gameName and tagLine):
        riotID = input("Riot ID: ")
        riotID = riotID.split('#')
        gameName = riotID[0]
        tagLine = riotID[1]

    params = {
        'api_key': API_KEY
    }
    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    
    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting account data from API: {e}')
        return None
    
def get_summoner_info(encryptedPUUID, tagLine):
    
    """
    Wrapper for SUMMONER-V4 API Portal
    Gets Profile information by using PUUID gathered by get_account_info
    ::return:: Profile information as a dictionary or None if there's an issue
    """
    
    params = {
        'api_key': API_KEY
        }
    api_url = f"https://{tagLine}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
    
    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting profile data from API: {e}')
        return None
    
def get_match_ids_by_summoner_puuid(summoner_puuid, matches_count, region=DEFAULT_REGION):
    
    """
    Retrieve a list of match IDs for matches recently played by a Summoner.
    
    Args:
        summoner_puuid (str): The PUUID (Player Universially Unique ID) of the Summoner.
        matches_count (int): The number of match IDs to retrieve.
        region (str, optional): The region where the Summoner is located. Defaults to the value in DEFAULT_REGION
    
    
    Returns:
        list or None: A list of match Ids if successful, None if an error ocurs during the API request.
        
    Raises:
        requests.exceptions.RequestException: If there's an issue with the API request.
        
    Example:
        get_matches_by_summoner('sample_puuid', 10, 'americas')
    """
    params = {
        'api_key': API_KEY
        }
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids"
    
    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Issue getting Summoner match data from API: {e}")
        return None
    
def did_player_win_match (summoner_puuid, match_id, region=DEFAULT_REGION):
    
    params = {
        'api_key': API_KEY,
    }
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    
    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        match_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Issue getting match data from API: {e}")
        return None
    
    if summoner_puuid in match_data["metadata"]["participants"]:
        player_index = match_data["metadata"]["participants"].index(summoner_puuid)
    else:
        return None
    
    player_info = match_data['info']['participants'][player_index]
    return player_info['win']

def win_percent_of_last_20_games(gameName, region=DEFAULT_REGION, tagLine=DEFAULT_TAG_LINE):
    account = get_account_info(gameName=None, tagLine=None, region=DEFAULT_REGION)
    matches = get_match_ids_by_summoner_puuid(account['puuid'], 20, region)
    
    wins = 0
    for match in matches:
        if did_player_win_match(account['puuid'], match):
            wins += 1
                
    return (wins/len(matches))*100

gameName= 'Randomdude02'
tagLine= 'NA1'

account = get_account_info(gameName, tagLine, region=DEFAULT_REGION)

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
