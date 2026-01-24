from dash import html, dcc, callback, Input, Output, dash_table
from src.stats_service import *
from src.components.components.header import header
from src.components.components.filter import *

def dashboard_layout():
    teams, seasons, options_teams = get_variables()

    return html.Div([
        header(),
        filter(seasons, options_teams),

        html.Div([
            html.H3("🔍 Recherche Statistique Joueur", style={"marginTop": "20px", "color": "#1f2937"}),
            dcc.Input(id="player-search-input", type="text", placeholder="Entrez le nom d'un joueur (ex: LeBron)...", 
                     style={"width": "100%", "padding": "12px", "borderRadius": "8px", "border": "1px solid #d1d5db", "marginBottom": "20px"}),
            dash_table.DataTable(
                id="player-stats-table",
                columns=[
                    {"name": "Saison", "id": "season"},
                    {"name": "Joueur", "id": "player"},
                    {"name": "Points/M", "id": "points_per_game"},
                    {"name": "Passes/M", "id": "assists_per_game"},
                    {"name": "Rebonds/M", "id": "rebounds_per_game"}
                ],
                style_table={'overflowX': 'auto', 'borderRadius': '10px', 'overflow': 'hidden'},
                style_header={'backgroundColor': '#3b82f6', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center', 'padding': '10px'},
                page_size=10
            )
        ], style={"padding": "20px", "backgroundColor": "#f3f4f6", "margin": "20px", "borderRadius": "12px"}),
    ], style={"backgroundColor": "#f9fafb", "minHeight": "100vh", "fontFamily": "sans-serif"})

@callback(Output("player-stats-table", "data"), Input("player-search-input", "value"))
def update_player_table(search_value):
    if not search_value: return []
    return get_player_stats(search_value).to_dict('records')

