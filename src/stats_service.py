import pandas as pd
import os

def load_all_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned")
    
    df_f = pd.read_csv(os.path.join(DATA_PATH, 'franchises.csv'))
    df_g = pd.read_csv(os.path.join(DATA_PATH, 'games.csv'))
    df_w = pd.read_csv(os.path.join(DATA_PATH, 'wins.csv'))
    df_p = pd.read_csv(os.path.join(DATA_PATH, 'players_stats.csv'))
    df_c = pd.read_csv(os.path.join(DATA_PATH, 'cities.csv'))
    return df_f, df_g, df_w, df_p, df_c

def get_team_list():
    df_f, _, _, _, _ = load_all_data()
    return sorted(df_f['franchise'].unique())

def get_season_list():
    _, df_g, _, _, _ = load_all_data()
    seasons = sorted(df_g['year'].unique(), reverse=True)
    return ["ALL-TIME"] + [str(s) for s in seasons]

def get_points_per_game(team, season):
    df_f, _, _, df_p, _ = load_all_data()
    df_p['season'] = pd.to_numeric(df_p['season'], errors='coerce')
    
    if str(season) == "ALL-TIME":
        df_season = df_p.copy()
    else:
        df_season = df_p[df_p['season'] == int(season)].copy()

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
    _, df_g, _, _, _ = load_all_data()
    df_g['year'] = pd.to_numeric(df_g['year'], errors='coerce')
    
    if str(season) == "ALL-TIME":
        df_season = df_g.copy()
    else:
        df_season = df_g[df_g['year'] == int(season)].copy()
    
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
    _, _, df_w, _, _ = load_all_data()
    if str(season) == "ALL-TIME":
        return df_w.sort_values('year', ascending=False).head(1)
    
    return df_w[df_w['year'] == int(season)]

def get_player_stats(player_name):
    _, _, _, df_p, _ = load_all_data()
    if player_name:
        return df_p[df_p['player'].str.contains(player_name, case=False, na=False)]
    return pd.DataFrame()

def get_finals_history(team="ALL"):
    _, _, df_w, _, _ = load_all_data()
    if team == "ALL": return df_w
    nickname = str(team).split()[-1].strip()
    return df_w[(df_w['champion'].astype(str).str.contains(nickname, case=False, na=False)) | 
                (df_w['west_champion'].astype(str).str.contains(nickname, case=False, na=False)) | 
                (df_w['east_champion'].astype(str).str.contains(nickname, case=False, na=False))]