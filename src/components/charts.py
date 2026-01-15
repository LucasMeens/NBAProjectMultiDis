from dash import dcc, html, dash_table

def charts_block():
    return html.Div([
        # Rangée des graphiques (Points, Victoires, Ratio)
        html.Div([
            html.Div([dcc.Graph(id="pts-hist")], style={"width": "33%"}),
            html.Div([dcc.Graph(id="wins-hist")], style={"width": "33%"}),
            html.Div([dcc.Graph(id="ratio-pie")], style={"width": "33%"}),
        ], style={"display": "flex"}),

        # Section Tableaux (Finales à gauche, Joueurs à droite)
        html.Div([
            # GAUCHE : Historique des champions
            html.Div([
                html.H3("Historique des Finales"),
                dash_table.DataTable(
                    id='finals-table',
                    columns=[{"name": i, "id": i} for i in ["year", "west_champion", "east_champion", "champion", "mvp", "mvp_team"]],
                    style_table={'height': '400px', 'overflowY': 'auto'},
                    style_header={'backgroundColor': '#111827', 'color': 'white', 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left', 'padding': '10px'}
                )
            ], style={"width": "60%", "padding": "10px"}),

            # DROITE : Recherche Joueur
            html.Div([
                html.H3("Recherche Statistique Joueur"),
                dcc.Input(id="player-search-input", value="LeBron James", type="text", 
                          style={"width": "100%", "padding": "10px", "marginBottom": "10px"}),
                dash_table.DataTable(
                    id='player-stats-table',
                    columns=[{"name": i, "id": i} for i in ["season", "player", "points_per_game", "assists_per_game", "rebounds_per_game"]],
                    style_table={'height': '400px', 'overflowY': 'auto'},
                    style_header={'backgroundColor': '#1f2937', 'color': 'white'}
                )
            ], style={"width": "38%", "padding": "10px"})
        ], style={"display": "flex", "marginTop": "30px"})
    ])