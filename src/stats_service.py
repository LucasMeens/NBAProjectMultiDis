import pandas as pd
import os

franchises = None
games = None
wins = None
players = None
cities = None

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

def is_data_loaded():
    if franchises is None:
        load_all_data()

def get_team_list():
    is_data_loaded()
    return sorted(franchises['franchise'].unique())

def get_season_list():
    is_data_loaded()
    seasons = sorted([s for s in games['year'].unique() if s <= 2018], reverse=True)
    return ["ALL-TIME"] + [str(s) for s in seasons]


def get_points_per_game(team, season):
    is_data_loaded()
    df_games = get_home_away_stats(team, season)
    
    if df_games is None or df_games.empty:
        return pd.DataFrame(columns=['score_obtenu'])

    def extract_score(row):
        keywords_map = {
            "Oklahoma City": ["Thunder", "SuperSonics", "Seattle"],
            "New Orleans Pelicans": ["Pelicans", "Hornets", "New Orleans"],
            "Los Angeles Clippers": ["Clippers", "San Diego"]
        }

        team_keywords = keywords_map.get(team, [str(team).split()[-1]])
        home_name_lower = str(row['home_name']).lower()
        
        is_home = False
        for k in team_keywords:
            if str(k).lower() in home_name_lower:
                is_home = True
                break
        
        return row['home_score'] if is_home else row['away_score']

   
    df_result = pd.DataFrame(df_games.to_dict()) 
    
    df_result['score_obtenu'] = df_result.apply(extract_score, axis=1)
    return df_result

# Fonction points_per_game for players (option finalement non envisagé) --------------------------------------------------

#    players['season'] = pd.to_numeric(players['season'], errors='coerce')
    
#    if str(season) == "ALL-TIME":
#        df_season = players.copy()
#    else:
#       df_season = players[players['season'] == int(season)].copy()

#    if team == "ALL":
#        return df_season[df_season['team_id'] != 'TOT']

#    historical_codes = {
#        "Oklahoma City Thunder": ["OKC", "SEA"],
#        "Oklahoma City": ["OKC", "SEA"],
#        "New Orleans Pelicans": ["NOP", "NOH", "NOK"], # NOK = New Orleans/OKC Hornets
#        "Los Angeles Clippers": ["LAC", "SDC", "BUF"],
#        "Brooklyn Nets": ["BRK", "NJN"],
#        "Charlotte Hornets": ["CHO", "CHA", "CHH"]
#    }
    
#    target_codes = historical_codes.get(team, [team[:3].upper()])

#    return df_season[df_season['team_id'].isin(target_codes)].copy()

## --------------------------------------------------------------------------------

def get_home_away_stats(team, season):
    is_data_loaded()
    games['year'] = pd.to_numeric(games['year'], errors='coerce')
    
    if str(season) == "ALL-TIME":
        df_season = games
    else:
        df_season = games[games['year'] == int(season)].copy()
    
    if team != "ALL":
        keywords = {
            "Oklahoma City": ["Thunder", "SuperSonics", "Seattle"],
            "Oklahoma City Thunder": ["Thunder", "SuperSonics", "Seattle"],
            "New Orleans Pelicans": ["Pelicans", "Hornets", "New Orleans"],
            "Los Angeles Clippers": ["Clippers", "San Diego", "Buffalo"],
            "Charlotte Hornets": ["Hornets", "Bobcats", "Charlotte"],
            "Brooklyn Nets": ["Nets", "New Jersey", "New York Nets"]
        }
        
        words = keywords.get(team, [str(team).split()[-1].strip()])
        
        pattern = "|".join(words)
        
        mask = (df_season['home_name'].str.contains(pattern, case=False, na=False)) | \
               (df_season['away_name'].str.contains(pattern, case=False, na=False))
        
        return df_season[mask].copy().reset_index(drop=True)
    
    return df_season

def get_finals_summary(season):
    is_data_loaded()
    if str(season) == "ALL-TIME":
        return wins.sort_values('year', ascending=False).head(1)
    
    return wins[wins['year'] == int(season)]

def get_player_stats(player_name):
    is_data_loaded()
    if player_name:
        return players[players['player'].str.contains(player_name, case=False, na=False)]
    
    return pd.DataFrame()

def get_finals_history(team="ALL"):
    is_data_loaded()
    if team == "ALL": 
        return wins
    
    nickname = str(team).split()[-1].strip()

    return wins[(wins['champion'].astype(str).str.contains(nickname, case=False, na=False)) | 
                (wins['west_champion'].astype(str).str.contains(nickname, case=False, na=False)) | 
                (wins['east_champion'].astype(str).str.contains(nickname, case=False, na=False))]

def load_map_data():
    is_data_loaded()
    return franchises, cities