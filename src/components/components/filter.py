from dash import html, dcc
from src.stats_service import get_team_list, get_season_list


def filter():
    teams = get_team_list()
    seasons = get_season_list()
    options_teams = [{"label": "🏀 Toutes les franchises", "value": "ALL"}] + [{"label": t, "value": t} for t in teams]

    html.Div([
            html.Label("Franchise", style={"fontWeight": "bold", "color": "#1f2937"}),
            dcc.Dropdown(id="team-dropdown", options=options_teams, value="ALL", clearable=False, style={"marginBottom": "15px"}),
            html.Label("Saison", style={"fontWeight": "bold", "color": "#1f2937"}),
            dcc.Dropdown(id="season-dropdown", options=[{"label": str(s), "value": s} for s in seasons], value=seasons[0]),
            html.Label("Options Carte", style={"marginTop": "15px", "fontWeight": "bold", "display": "block"}),
            dcc.Checklist(id="map-options", options=[{"label": " Afficher densité population", "value": "density"}], value=[], style={"padding": "10px 0"}),
    ], style={"width": "28%", "display": "inline-block", "verticalAlign": "top", "padding": "20px", "backgroundColor": "white", "borderRadius": "12px", "boxShadow": "0 4px 6px -1px rgba(0,0,0,0.1)"}),