import kagglehub as kg
import shutil
from pathlib import Path

# Downloading NBA Finals and MVP.csv
path_fnm = kg.dataset_download("thedevastator/historical-nba-finals-and-mvp-results")
finals_n_mvp = Path(path_fnm) / "NBA Finals and MVP.csv"
dest_fnm = Path("data/raw/csvs/finals_n_mvp.csv")
dest_fnm.parent.mkdir(parents=True, exist_ok=True) # check if the parents folders exist and create it if not
shutil.copy(finals_n_mvp, dest_fnm)

# Downloading games.csv
path_g = kg.dataset_download("eoinamoore/historical-nba-data-and-player-box-scores")
games = Path(path_g) / "Games.csv"
dest_g = Path("data/raw/csvs/games.csv")
# No need of checking parent here because we did it earlier
shutil.copy(games, dest_g)  

# Downloading schedule2026.csv
schedule = Path(path_g) / "LeagueSchedule25_26.csv"
dest_s = Path("data/raw/csvs/schedule26.csv")
# No need of checking parent here because we did it earlier
shutil.copy(schedule, dest_s)

# Downloading franchise_locations.csv
path_fl = kg.dataset_download("logandonaldson/sports-stadium-locations")
locations = Path(path_fl) / "stadiums.csv"
dest_fl = Path("data/raw/csvs/franchise_locations.csv")
# No need of checking parent here because we did it earlier
shutil.copy(locations, dest_fl)

# Downloading nba_player_stats.csv
path_pl = kg.dataset_download("robertsunderhaft/nba-player-season-statistics-with-mvp-win-share")
stats = Path(path_pl) / "NBA_Dataset.csv"
dest_ps = Path("data/raw/csvs/nba_player_stats.csv")
# No need of checking parent here because we did it earlier
shutil.copy(stats, dest_s)
