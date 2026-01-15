from dash import html, dcc, callback, Input, Output
from src.backend.stats_service import get_team_list, get_season_list, get_franchise_locations
from src.frontend.components.header import header
from src.frontend.components.nba_map_bokeh import nba_map_component
from src.frontend.components.charts import charts_block
from src.frontend.components.team_cards import team_cards_component

import plotly.express as px
from src.backend.stats_service import (
    get_population_vs_wins,
    get_home_away_wins,
    get_points_per_game,
    get_finals_wins,
    get_finals_details,
)


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

def dashboard_layout():
    teams = get_team_list()

    return html.Div(
        [
            header(),

            # -----------------------
            # Filtres + Team Cards
            # -----------------------
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Franchise"),
                            dcc.Dropdown(
                                id="team-dropdown",
                                options=[{"label": t, "value": t} for t in teams],
                                value=teams[0] if teams else None,
                            ),

                            html.Label("Saison", style={"marginTop": "10px"}),
                            dcc.Dropdown(id="season-dropdown"),
                        ],
                        style={
                            "width": "30%",
                            "display": "inline-block",
                            "verticalAlign": "top",
                        },
                    ),

                    html.Div(
                        [team_cards_component()],
                        style={
                            "width": "68%",
                            "display": "inline-block",
                            "marginLeft": "2%",
                        },
                    ),
                ],
                style={"padding": "20px"},
            ),

            # -----------------------
            # Carte NBA
            # -----------------------
            html.Div([nba_map_component()], style={"padding": "0 20px"}),

            # -----------------------
            # Graphiques dynamiques
            # -----------------------
            html.Div([charts_block()], style={"padding": "0 20px"}),

        ],
        style={"backgroundColor": "#f3f4f6", "minHeight": "100vh"},
    )


# ============================================================
# CALLBACKS
# ============================================================

# -----------------------
# Dropdown saisons
# -----------------------
@callback(
    Output("season-dropdown", "options"),
    Output("season-dropdown", "value"),
    Input("team-dropdown", "value"),
)
def update_season_dropdown(team):
    if team is None:
        return [], None

    seasons = get_season_list(team)
    return (
        [{"label": s, "value": s} for s in seasons],
        seasons[0] if seasons else None,
    )



# -----------------------
# Corrélation population ↔ titres
# -----------------------
@callback(
    Output("population-victory-correlation", "figure"),
    Input("team-dropdown", "value"),
)
def update_population_correlation(_team):
    df = get_population_vs_wins()

    fig = px.scatter(
        df,
        x="population",
        y="titles",
        color="franchise",
        size="population",
        hover_name="franchise",
        title="Population de la ville vs titres NBA",
    )
    return fig


# -----------------------
# Victoires domicile / extérieur
# -----------------------
@callback(
    Output("home-away-wins", "figure"),
    Input("team-dropdown", "value"),
    Input("season-dropdown", "value"),
)
def update_home_away(team, season):
    if team is None or season is None:
        return px.histogram(title="Sélectionnez une franchise et une saison")

    df = get_home_away_wins(team, season)
    if df.empty:
        return px.histogram(title=f"Aucune donnée pour {team} - {season}")

    fig = px.histogram(
        df,
        x="home_away",
        color="home_away",
        title=f"Victoires domicile / extérieur ({team}, {season})",
    )
    return fig


# -----------------------
# Points par match
# -----------------------
@callback(
    Output("points-per-game", "figure"),
    Input("team-dropdown", "value"),
    Input("season-dropdown", "value"),
)
def update_points(team, season):
    if team is None or season is None:
        return px.histogram(title="Sélectionnez une franchise et une saison")

    df = get_points_per_game(team, season)
    if df.empty:
        return px.histogram(title=f"Aucune donnée de points pour {team} - {season}")

    fig = px.histogram(
        df,
        x="points",
        nbins=20,
        title=f"Distribution des points par match ({team}, {season})",
    )
    return fig


# -----------------------
# Nombre de titres
# -----------------------
@callback(
    Output("finals-wins-counter", "figure"),
    Input("team-dropdown", "value"),
)
def update_titles(team):
    if team is None:
        return px.bar(title="Sélectionnez une franchise")

    df = get_finals_wins(team)
    fig = px.bar(
        x=["Titres NBA"],
        y=[len(df)],
        title=f"Nombre de titres NBA ({team})",
    )
    return fig


# -----------------------
# Détail des finales
# -----------------------
@callback(
    Output("finals-details", "figure"),
    Input("team-dropdown", "value"),
)
def update_finals_details_chart(team):
    if team is None:
        return px.scatter(title="Sélectionnez une franchise")

    df = get_finals_details(team)
    if df.empty:
        return px.scatter(title=f"Aucune finale gagnée pour {team}")

    fig = px.bar(
        df,
        x="year",
        y="wins",
        hover_data=["opponent", "mvp"],
        title=f"Détails des finales gagnées ({team})",
    )
    return fig
