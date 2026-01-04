import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/nba_player_stats_raw.csv")
CLEAN_DATA_PATH = Path("data/cleaned/nba_players.csv")

COLUMNS_TO_KEEP = [
    "season", "player", "pos", "age", "team_id",
    "g", "mp_per_g",
    "pts_per_g", "ast_per_g", "trb_per_g",
    "fg_pct", "fg3_pct", "ft_pct",
    "stl_per_g", "blk_per_g",
    "per", "ws", "vorp"
]

NUMERIC_COLUMNS = [
    col for col in COLUMNS_TO_KEEP
    if col not in ["season", "player", "pos", "team_id"]
]

def clean_players_dataset():
    print(" Chargement du dataset brut")
    df = pd.read_csv(RAW_DATA_PATH)

    print(f" Taille initiale : {df.shape}")

    df = df[COLUMNS_TO_KEEP]

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["player", "season", "pts_per_g"])
    df["season"] = df["season"].astype(int)
    df = df[df["season"] >= 1970]

    df = df.fillna(0)

    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DATA_PATH, index=False)

    print(f"Dataset clean généré : {CLEAN_DATA_PATH}")
    print(f" Taille finale : {df.shape}")

if __name__ == "__main__":
    clean_players_dataset()
