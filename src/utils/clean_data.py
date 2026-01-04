import pandas as pd

# Cleaning and writing the "cities.csv" file for population density

us_cities = pd.read_csv("NBAProjectMultiDis/data/raw/csvs/uscities.csv")
canada_cities = pd.read_csv("NBAProjectMultiDis/data/raw/csvs/canadacities.csv")

us_select = us_cities[["city", "density", "lat", "lng"]]
canada_select = canada_cities[["city", "density", "lat", "lng"]]

concatenation = pd.concat([us_select, canada_select], ignore_index=True)

concatenation_unique = (
    concatenation
    .assign(city=concatenation["city"].str.strip().str.title()) # Preventing duplicate caused by merging different datasets
    .sort_values("density", ascending=False)
    .drop_duplicates(subset="city")
)

concatenation_unique.to_csv("NBAProjectMultiDis/data/cleaned/cities.csv", index=False)

# Cleaning and writing the "franchises.csv" file for NBA franchises location

franchises = pd.read_csv("NBAProjectMultiDis/data/raw/csvs/franchise_locations.csv")

NBA = franchises[franchises["League"] == "NBA"]
selection = NBA[["Team", "Lat", "Long"]]

selection = selection.rename(columns={
    "Team":"franchise",
    "Lat": "lat",
    "Long": "lng"
})

selection.to_csv("NBAProjectMultiDis/data/cleaned/franchises.csv", index=False)

# Cleaning and writing the "wins.csv" file for NBA finals, winners, mvp, etc..

wins = pd.read_csv("NBAProjectMultiDis/data/raw/csvs/NBA Finals and MVP.csv")

wins = wins.rename(columns={
    "Year": "year",
    "Western Champion": "west_champion",
    "Eastern Champion": "east_champion",
    "Result": "result",
    "NBA Champion": "champion",
    "MVP Name": "mvp",
    "MVP Team": "mvp_team",
})

wins_selected = wins[["year", "west_champion", "east_champion", "result", "champion", "mvp", "mvp_team"]]

wins_selected.to_csv("NBAProjectMultiDis/data/cleaned/wins.csv", index=False)

# Cleaning and writing the "games.csv" file for our graphics on points averages by year
# 21800549

games = pd.read_csv(
    "NBAProjectMultiDis/data/raw/csvs/games.csv",
    usecols=[
        "hometeamCity",
        "hometeamName",
        "awayteamCity",
        "awayteamName",
        "homeScore",            # To avoid warning about columns that're not used
        "awayScore",
        "winner",
        "hometeamId",
        "awayteamId"
    ]
)

games = games.rename(columns={
    "hometeamCity": "home_city",
    "hometeamName": "home_name",
    "awayteamCity": "away_city",
    "awayteamName": "away_name",
    "homeScore": "home_score",
    "awayScore": "away_score",
})

def get_winner(row):
    if row["winner"] == row["hometeamId"]:
        return row["home_name"]
    elif row["winner"] == row["awayteamId"]:
        return row["away_name"]
    else:
        return None

games["winner_name"] = games.apply(get_winner, axis=1)

games_selected = games[["home_city", "home_name", "away_city", "away_name", "home_score", "away_score", "winner_name"]]

games_selected.to_csv("NBAProjectMultiDis/data/cleaned/games.csv", index=False)
