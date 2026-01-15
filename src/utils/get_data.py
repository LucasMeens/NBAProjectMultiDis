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
