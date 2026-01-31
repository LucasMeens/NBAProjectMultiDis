import kagglehub as kg
import shutil
from pathlib import Path
import requests
import zipfile
import io
import os

def download():
    # ----------------------------------
    # Downloading NBA Finals and MVP.csv
    # ----------------------------------

    # Download the dataset using kagglehub
    path_fnm = kg.dataset_download("thedevastator/historical-nba-finals-and-mvp-results")
    # Getting the good file if it's a dataset
    finals_n_mvp = Path(path_fnm) / "NBA Finals and MVP.csv"

    # Setting the destination as data/raw/csvs
    dest_fnm = Path("data/raw/csvs/finals_n_mvp.csv")
    # Check if the parents folders exist and create it if not
    dest_fnm.parent.mkdir(parents=True, exist_ok=True)

    # Copy the file in the right destination
    shutil.copy(finals_n_mvp, dest_fnm)

    # ----------------------------------
    # Downloading games.csv
    # ----------------------------------

    # Download the dataset using kagglehub
    path_g = kg.dataset_download("eoinamoore/historical-nba-data-and-player-box-scores")
    # Getting the good file because here, it's a dataset
    games = Path(path_g) / "Games.csv"

    # Setting the destination as data/raw/csvs
    dest_g = Path("data/raw/csvs/games.csv")

    # No need of checking parent here because we did it earlier

    # Copy the file in the right destination
    shutil.copy(games, dest_g)

    # ----------------------------------
    # Downloading franchise_locations.csv
    # ----------------------------------

    # Download the dataset using kagglehub
    path_fl = kg.dataset_download("logandonaldson/sports-stadium-locations")
    # Getting the good file because here, it's a dataset
    locations = Path(path_fl) / "stadiums.csv" 

    # Setting the destination as data/raw/csvs
    dest_fl = Path("data/raw/csvs/franchise_locations.csv")

    # No need of checking parent here because we did it earlier

    # Copy the file in the right destination
    shutil.copy(locations, dest_fl)

    # ----------------------------------
    # Downloading nba_player_stats.csv
    # ----------------------------------

    # Download the dataset using kagglehub
    path_pl = kg.dataset_download("robertsunderhaft/nba-player-season-statistics-with-mvp-win-share")
    # Getting the good file because here, it's a dataset
    stats = Path(path_pl) / "NBA_Dataset.csv"

    # Setting the destination as data/raw/csvs
    dest_ps = Path("data/raw/csvs/nba_player_stats.csv")

    # No need of checking parent here because we did it earlier

    # Copy the file in the right destination
    shutil.copy(stats, dest_ps)

    # ----------------------------------
    # Downloading canada_cities.csv
    # ----------------------------------

    # Getting the downloading url of the csv file
    can_url = "https://simplemaps.com/static/data/canada-cities/1.8/basic/simplemaps_canadacities_basicv1.8.zip"

    # Setting the destination as data/raw/csvs
    dest_cc = Path("data/raw/csvs")

    # Adding a header so we make ourselves like we are a browser and to be able to download
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    # Downloading the csv file
    can_cities = requests.get(can_url, headers=headers) 
    # Warning us if the download fail
    can_cities.raise_for_status()

    # Using zipFile to extract the folder downloaded
    with zipfile.ZipFile(io.BytesIO(can_cities.content)) as ref_can:
        ref_can.extractall(dest_cc)

    # Renaming the files that interest us
    name = dest_cc / "canadacities.csv"
    new_name = dest_cc / "canada_cities.csv"
    name.rename(new_name)

    # Removing the others files that has been extracted and that we don't need
    os.remove(Path("data/raw/csvs/license.txt"))
    os.remove(Path("data/raw/csvs/canadacities.sql"))
    os.remove(Path("data/raw/csvs/canadacities.xlsx"))

    # ----------------------------------
    # Downloading us_cities.csv
    # ----------------------------------

    # Getting the downloading url of the csv file
    us_url = "https://simplemaps.com/static/data/us-cities/1.92/basic/simplemaps_uscities_basicv1.92.zip"

    # Setting the destination as data/raw/csvs
    dest_uc = Path("data/raw/csvs")

    # Downloading the csv file
    us_cities = requests.get(us_url, headers=headers)
    # Warn if the download fail
    us_cities.raise_for_status()

    # Using zipFile to extract the folder downloaded
    with zipfile.ZipFile(io.BytesIO(us_cities.content)) as ref_us:
        ref_us.extractall(dest_uc)

    # Renaming the files that interest us
    name = dest_cc / "uscities.csv"
    new_name = dest_cc / "us_cities.csv"
    name.rename(new_name)

    # Removing the others files that has been extracted and that we don't need
    os.remove(Path("data/raw/csvs/license.txt"))
    os.remove(Path("data/raw/csvs/uscities.xlsx"))

