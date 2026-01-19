import kagglehub as kg
import shutil
from pathlib import Path
import requests
import zipfile
import io
import os
# ----------------------------------
# Downloading NBA Finals and MVP.csv
# ----------------------------------

path_fnm = kg.dataset_download("thedevastator/historical-nba-finals-and-mvp-results") # Download the dataset using kagglehub
finals_n_mvp = Path(path_fnm) / "NBA Finals and MVP.csv" # Getting the good file if it's a dataset

dest_fnm = Path("data/raw/csvs/finals_n_mvp.csv") # Setting the destination as data/raw/csvs
dest_fnm.parent.mkdir(parents=True, exist_ok=True) # Check if the parents folders exist and create it if not

shutil.copy(finals_n_mvp, dest_fnm) # Copy the file in the right destination

# ----------------------------------
# Downloading games.csv
# ----------------------------------

path_g = kg.dataset_download("eoinamoore/historical-nba-data-and-player-box-scores") # Download the dataset using kagglehub
games = Path(path_g) / "Games.csv" # Getting the good file because here, it's a dataset

dest_g = Path("data/raw/csvs/games.csv") # Setting the destination as data/raw/csvs
# No need of checking parent here because we did it earlier

shutil.copy(games, dest_g) # Copy the file in the right destination

# ----------------------------------
# Downloading franchise_locations.csv
# ----------------------------------

path_fl = kg.dataset_download("logandonaldson/sports-stadium-locations") # Download the dataset using kagglehub
locations = Path(path_fl) / "stadiums.csv" # Getting the good file because here, it's a dataset

dest_fl = Path("data/raw/csvs/franchise_locations.csv") # Setting the destination as data/raw/csvs
# No need of checking parent here because we did it earlier

shutil.copy(locations, dest_fl) # Copy the file in the right destination

# ----------------------------------
# Downloading nba_player_stats.csv
# ----------------------------------

path_pl = kg.dataset_download("robertsunderhaft/nba-player-season-statistics-with-mvp-win-share") # Download the dataset using kagglehub
stats = Path(path_pl) / "NBA_Dataset.csv" # Getting the good file because here, it's a dataset

dest_ps = Path("data/raw/csvs/nba_player_stats.csv") # Setting the destination as data/raw/csvs
# No need of checking parent here because we did it earlier

shutil.copy(stats, dest_ps) # Copy the file in the right destination

# ----------------------------------
# Downloading canada_cities.csv
# ----------------------------------

can_url = "https://simplemaps.com/static/data/canada-cities/1.8/basic/simplemaps_canadacities_basicv1.8.zip" # Downloading url of the csv file

dest_cc = Path("data/raw/csvs") # Setting the destination as data/raw/csvs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
can_cities = requests.get(can_url, headers=headers) # Download the csv file
can_cities.raise_for_status()      # Warn if the download fail

with zipfile.ZipFile(io.BytesIO(can_cities.content)) as ref_can:
    ref_can.extractall(dest_cc)

name = dest_cc / "canadacities.csv"
new_name = dest_cc / "canada_cities.csv"
name.rename(new_name)

os.remove(Path("data/raw/csvs/license.txt"))
os.remove(Path("data/raw/csvs/canadacities.sql"))
os.remove(Path("data/raw/csvs/canadacities.xlsx"))

# ----------------------------------
# Downloading us_cities.csv
# ----------------------------------

us_url = "https://simplemaps.com/static/data/us-cities/1.92/basic/simplemaps_uscities_basicv1.92.zip"
dest_uc = Path("data/raw/csvs")

us_cities = requests.get(us_url, headers=headers)
us_cities.raise_for_status()      # Warn if the download fail
with zipfile.ZipFile(io.BytesIO(us_cities.content)) as ref_us:
    ref_us.extractall(dest_uc)
name = dest_cc / "uscities.csv"
new_name = dest_cc / "us_cities.csv"
name.rename(new_name)
os.remove(Path("data/raw/csvs/license.txt"))
os.remove(Path("data/raw/csvs/uscities.xlsx"))

