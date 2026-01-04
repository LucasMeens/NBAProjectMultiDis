from dash import html, dcc
import plotly.express as px
from src.backend.stats_service import load_players, get_shot_heatmap

def players_layout():
    players_df = load_players()
    player_list = players_df["Player"].unique()

    heat_df = get_shot_heatmap(player_list[0])

    fig_heat = px.density_heatmap(
        heat_df,
        x="X",
        y="Y",
        z="MadeShot",
        title="Heatmap des tirs"
    )

    return html.Div([
        html.H2("Recherche joueur"),

        dcc.Dropdown(
            options=[{"label": p, "value": p} for p in player_list],
            value=player_list[0]
        ),

        dcc.Graph(figure=fig_heat)
    ])
