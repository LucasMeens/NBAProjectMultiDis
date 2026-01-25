import dash 
from dash import html, dcc, callback, Input, Output, dash_table
from src.stats_service import get_player_stats
from src.components.components.header import header

dash.register_page(__name__)

def layout():
    return html.Div(
    [
        header(),

        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "🔍 Statistique des Joueurs", 
                            className="player-title"
                        ),
                        dcc.Input(
                            id="player-search-input", 
                            type="text", 
                            placeholder="Entrez le nom d'un joueur (ex: LeBron)...", 
                            className="players-input"
                        ),
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
                    ],
                    className="container-div"
                ), 
            ],
            className="flex-box"
        )
    ], 
    style={
        "backgroundColor" : "#1D428A"
    }
),

@callback(
    Output("player-stats-table", "data"), 
    Input("player-search-input", "value")
)
def update_player_table(search_value):
    if not search_value: 
        return []
    
    return get_player_stats(search_value).to_dict('records')