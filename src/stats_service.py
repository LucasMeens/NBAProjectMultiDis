import pandas as pd

def load_all_data():
    df_f = pd.read_csv('data/cleaned/franchises.csv')
    df_g = pd.read_csv('data/cleaned/games.csv')
    df_w = pd.read_csv('data/cleaned/wins.csv')
    
    try:
        df_p = pd.read_csv('data/cleaned/players_stats.csv')
    except:
        df_p = pd.DataFrame(columns=['player', 'pts', 'reb', 'ast'])
        
    return df_f, df_g, df_w, df_p 