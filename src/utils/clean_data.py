import pandas as pd

# Cleaning and writing the "cities.csv" file for population density

us_cities = pd.read_csv("data/raw/csvs/us_cities.csv")
canada_cities = pd.read_csv("data/raw/csvs/canada_cities.csv")

us_select = us_cities[["city", "density", "lat", "lng"]]
canada_select = canada_cities[["city", "density", "lat", "lng"]]

concatenation = pd.concat([us_select, canada_select], ignore_index=True)

concatenation_unique = (
    concatenation
    .assign(city=concatenation["city"].str.strip().str.title()) # Preventing duplicate caused by merging different datasets
    .sort_values("density", ascending=False)
    .drop_duplicates(subset="city")
)

concatenation_unique.to_csv("data/cleaned/cities.csv", index=False)

# Cleaning and writing the "franchises.csv" file for NBA franchises location

franchises = pd.read_csv("data/raw/csvs/franchise_locations.csv")

NBA = franchises[franchises["League"] == "NBA"]
selection = NBA[["Team", "Lat", "Long"]]

selection = selection.rename(columns={
    "Team":"franchise",
    "Lat": "lat",
    "Long": "lng"
})

selection.to_csv("data/cleaned/franchises.csv", index=False)

# Cleaning and writing the "wins.csv" file for NBA finals, winners, mvp, etc..

wins = pd.read_csv("data/raw/csvs/finals_n_mvp.csv")

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

wins_selected.to_csv("data/cleaned/wins.csv", index=False)

# Cleaning and writing the "games.csv" file for our graphics on points averages by year
# 21800549

games = pd.read_csv(
    "data/raw/csvs/games.csv",
    usecols=[
        "hometeamCity",
        "hometeamName",
        "awayteamCity",
        "awayteamName",
        "homeScore",            # To avoid warning about columns that're not used
        "awayScore",
        "winner",
        "hometeamId",
        "awayteamId",
        "gameDateTimeEst"
    ]
)

games = games.rename(columns={
    "hometeamCity": "home_city",
    "hometeamName": "home_name",
    "awayteamCity": "away_city",
    "awayteamName": "away_name",
    "homeScore": "home_score",
    "awayScore": "away_score",
    "gameDateTimeEst" : "year",
})

def get_winner(row):
    if row["winner"] == row["hometeamId"]:
        return row["home_name"]
    elif row["winner"] == row["awayteamId"]:
        return row["away_name"]
    else:
        return None

games["winner_name"] = games.apply(get_winner, axis=1)
games["year"] = games["year"].str[:4]

games_selected = games[["year", "home_city", "home_name", "away_city", "away_name", "home_score", "away_score", "winner_name"]]

games_selected.to_csv("data/cleaned/games.csv", index=False)
# Cleaning and writing 'players.csv' file for player's stat

players_stats = pd.read_csv("data/raw/csvs/nba_player_stats.csv")

players_selected = players_stats[[
    "season", "player", "pos", "age", 
    "team_id", "g", "mp_per_g", "pts_per_g",
    "ast_per_g", "trb_per_g", "stl_per_g", "blk_per_g",
    "fg_pct", "fg3_pct", "ft_pct"
]]

players_selected = players_selected.rename(columns={
    "g" : "games",
    "mp_per_g" : "min_per_game",
    "pts_per_g" : "points_per_game",
    "ast_per_g" : "assists_per_game",
    "trb_per_g" : "rebounds_per_game",
    "stl_per_g" : "steals_per_game",
    "blk_per_g" : "blocks_per_game",
    "fg_pct" : "bucket2_percentage",
    "fg3_pct" : "bucket3_percentage",
    "ft_pct" : "total_percentage",
})

players_selected.to_csv("data/cleaned/players_stats.csv", index=False)


