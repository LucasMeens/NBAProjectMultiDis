import pandas as pd

def load_all_data():
    # Chargement des 4 fichiers indispensables
    df_f = pd.read_csv('data/cleaned/franchises.csv')
    df_g = pd.read_csv('data/cleaned/games.csv')
    df_w = pd.read_csv('data/cleaned/wins.csv')
    
    # On ajoute le chargement du 4ème fichier (joueurs)
    try:
        df_p = pd.read_csv('data/cleaned/players_stats.csv')
    except:
        # Si le fichier n'existe pas encore, on crée un dataframe vide pour éviter le crash
        df_p = pd.DataFrame(columns=['player', 'pts', 'reb', 'ast'])
        
    return df_f, df_g, df_w, df_p  # On renvoie bien les 4 ici