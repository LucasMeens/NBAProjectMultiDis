import pandas as pd
import os

franchises = ''
games = ''
wins = ''
players = ''
cities = ''

def load_all_data():
    global franchises
    global games
    global wins
    global players
    global cities

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned")
    
    franchises = pd.read_csv(os.path.join(DATA_PATH, 'franchises.csv'))
    games = pd.read_csv(os.path.join(DATA_PATH, 'games.csv'))
    wins = pd.read_csv(os.path.join(DATA_PATH, 'wins.csv'))
    players = pd.read_csv(os.path.join(DATA_PATH, 'players_stats.csv'))
    cities = pd.read_csv(os.path.join(DATA_PATH, 'cities.csv'))

load_all_data()

def get_team_list():
    return sorted(franchises['franchise'].unique())

def get_season_list():
    seasons = sorted(games['year'].unique(), reverse=True)
    return ["ALL-TIME"] + [str(s) for s in seasons]

def get_points_per_game(team, season):
    players['season'] = pd.to_numeric(players['season'], errors='coerce')
    
    if str(season) == "ALL-TIME":
        df_season = players.copy()
    else:
        df_season = players[players['season'] == int(season)].copy()

    if team == "ALL":
        return df_season[df_season['team_id'] != 'TOT']

    historical_codes = {
        "Oklahoma City Thunder": ["OKC", "SEA"],
        "Oklahoma City": ["OKC", "SEA"],
        "New Orleans Pelicans": ["NOP", "NOH", "NOK"], # NOK = New Orleans/OKC Hornets
        "Los Angeles Clippers": ["LAC", "SDC", "BUF"],
        "Brooklyn Nets": ["BRK", "NJN"],
        "Charlotte Hornets": ["CHO", "CHA", "CHH"]
    }
    
    target_codes = historical_codes.get(team, [team[:3].upper()])

    return df_season[df_season['team_id'].isin(target_codes)].copy()

def get_home_away_stats(team, season):
    games['year'] = pd.to_numeric(games['year'], errors='coerce')
    
    if str(season) == "ALL-TIME":
        df_season = games.copy()
    else:
        df_season = games[games['year'] == int(season)].copy()
    
    if team != "ALL":
        keywords = {
            "Oklahoma City": ["Thunder", "Sonics", "Seattle"],
            "New Orleans Pelicans": ["Pelicans", "Hornets", "New Orleans"],
            "Los Angeles Clippers": ["Clippers", "San Diego"],
            "Brooklyn Nets": ["Nets", "New Jersey"]
        }
        
        words = keywords.get(team, [str(team).split()[-1].strip()])
        
        pattern = "|".join(words)
        
        mask = (df_season['home_name'].str.contains(pattern, case=False, na=False)) | \
               (df_season['away_name'].str.contains(pattern, case=False, na=False))
        
        return df_season[mask].copy()
    
    return df_season

def get_finals_summary(season):
    if str(season) == "ALL-TIME":
        return wins.sort_values('year', ascending=False).head(1)
    
    return wins[wins['year'] == int(season)]

def get_player_stats(player_name):
    if player_name:
        return players[players['player'].str.contains(player_name, case=False, na=False)]
    
    return pd.DataFrame()

def get_finals_history(team="ALL"):
    if team == "ALL": 
        return wins
    
    nickname = str(team).split()[-1].strip()

    return wins[(wins['champion'].astype(str).str.contains(nickname, case=False, na=False)) | 
                (wins['west_champion'].astype(str).str.contains(nickname, case=False, na=False)) | 
                (wins['east_champion'].astype(str).str.contains(nickname, case=False, na=False))]