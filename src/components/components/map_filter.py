from dash import html, dcc
from src.stats_service import get_team_list, get_season_list

def get_variables():
    teams = get_team_list()
    options_teams = [{"label": "🏀 Toutes les franchises", "value": "ALL"}] + [{"label": t, "value": t} for t in teams]

    return (teams, options_teams)
    
def filter(options_teams):
    return html.Div(
        [
            html.Div(
                [
                    html.Label("Franchise", style={"fontWeight": "bold", "color": "#1f2937"}),
                    dcc.Dropdown(id="team-dropdown", options=options_teams, value="ALL", clearable=False, style={"marginBottom": "15px"}),
                    html.Label("Options Carte", style={"marginTop": "15px", "fontWeight": "bold", "display": "block"}),
                    dcc.Checklist(id="map-options", options=[{"label": " Afficher densité population", "value": "density"}], value=[], style={"padding": "10px 0"}),
                ],
                className="filter-container",
            )
        ],   
        className="flex-box"       
    )
