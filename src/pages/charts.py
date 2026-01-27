import dash
from dash import html, dcc, callback, Input, Output, dash_table
from src.components.components.filter import get_variables, filter
from src.components.components.header import header
from src.stats_service import *
import plotly.express as px
import plotly.graph_objects as go
from src.components.components.team_cards import team_cards_component

dash.register_page(__name__)

teams, seasons, options_teams = get_variables()

def layout():
    return html.Div(
    [
        header(),
        filter(seasons, options_teams),
        
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [       
                                html.Div(
                                    [
                                        team_cards_component()
                                    ], 
                                    style={
                                        "width": "68%", 
                                        "display": "inline-block",  # I don't know what is it so i let it for now
                                        "marginLeft": "3%"
                                    }
                                ),
                            ], 
                            style={
                                "padding": "20px", 
                                "display": "flex",              # I don't know what is it so i let it for now
                                "alignItems": "stretch"
                            }
                        ),

                        html.Div(
                            [ 
                                # ---------------------------------------
                                # First Graph : Points histogram
                                # ---------------------------------------
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="pts-hist",
                                                    config={'displayModeBar': False} # Masque la barre d'outils pour un look plus propre
                                                )
                                            ], 
                                            className="graph"
                                        )
                                    ], 
                                    className="one-graphs"
                                ),
                                
                                # ---------------------------------------
                                # Second Graph : Victory analysis
                                # ---------------------------------------
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="wins-hist",
                                                    config={'displayModeBar': False},
                                                ),
                                            ],
                                            className="graph"
                                        )
                                    ], 
                                    className="one-graphs"
                                ),
                                
                                # ---------------------------------------
                                # Third Graph : Wins/Lose Ratio
                                # ---------------------------------------        
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="ratio-pie",
                                                    config={'displayModeBar': False}
                                                )
                                            ],
                                            className="graph"
                                        )
                                    ], 
                                    className="other-graph"
                                ),

                            ], 
                            className="graphs-container"
                        ),

                        html.Div(
                            [
                                html.H2(
                                    "📜 Historique des Finales NBA", 
                                    className="data-table-title"
                                ),
                                dash_table.DataTable(
                                    id="finals-table",
                                    columns=[
                                        {"name": "Année", "id": "year"},
                                        {"name": "Champion Ouest", "id": "west_champion"},
                                        {"name": "Champion Est", "id": "east_champion"},
                                        {"name": "Vainqueur", "id": "champion"},
                                        {"name": "MVP", "id": "mvp"}
                                    ],
                                    style_table={'overflowX': 'auto', 'borderRadius': '10px', 'overflow': 'hidden'},
                                    style_header={'backgroundColor': '#1f2937', 'color': 'white', 'fontWeight': 'bold'},
                                    style_cell={'textAlign': 'center', 'fontFamily': 'sans-serif'},
                                    page_size=10
                                )
                            ], 
                        ),

                        html.Div(
                            id="finale-recap-container", 
                            className="finals-recap"
                        ), 
                    ],
                    className="charts-page"
                ),
            ],
            className="flex-box"
        ),
    ]
)



@callback(
    Output("pts-hist", "figure"), 
    [Input("team-dropdown", "value"), Input("season-dropdown", "value")]
)
def update_pts_hist(team, season):
    points = get_points_per_game(team, season)
    
    if points.empty:
        return go.Figure().update_layout(title="Aucune donnée trouvée")

    title = f"Points/Match : {team} ({season})"
    fig = px.histogram(points, x="points_per_game", nbins=20 if season == "ALL-TIME" else 10, 
                       title=title, color_discrete_sequence=['#3b82f6'],
                       hover_data=["player", "season"])
    
    fig.update_layout(bargap=0.1, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig

@callback(
    Output("wins-hist", "figure"), 
    [
        Input("team-dropdown", "value"), 
        Input("season-dropdown", "value")
    ]
)
def update_wins_analysis(team, season):
    all_games = get_home_away_stats("ALL", season)
    if team == "ALL":
        counts = all_games['winner_name'].value_counts().nlargest(10).reset_index()
        counts.columns = ['Equipe', 'Victoires']
        fig = px.bar(counts, x='Equipe', y='Victoires', title="Top 10 Victoires", color='Victoires', color_continuous_scale='Blues')
    else:
        nickname = str(team).split()[-1].strip()
        team_wins = all_games[all_games['winner_name'].astype(str).str.contains(nickname, case=False, na=False)].copy()

        if team_wins.empty: 
            return go.Figure(layout={"title": f"0 victoires pour {nickname}"})
        
        team_wins['Lieu'] = team_wins.apply(lambda r: '🏠 Domicile' if nickname.lower() in str(r['home_name']).lower() else '✈️ Extérieur', axis=1)
        
        data = team_wins['Lieu'].value_counts().reset_index()
        data.columns = ['Lieu', 'Victoires']
        
        fig = px.bar(data, x='Lieu', y='Victoires', title=f"Victoires : {team}", color='Lieu', color_discrete_map={'🏠 Domicile': '#1d4ed8', '✈️ Extérieur': '#60a5fa'})
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_x=0.5)
    
    return fig

@callback(
    Output("ratio-pie", "figure"), 
    [
        Input("team-dropdown", "value"), 
        Input("season-dropdown", "value")
    ]
)
def update_ratio_logic(team, season):
    if team == "ALL":
        games = get_home_away_stats("ALL", season)

        games['HomeWin'] = games.apply(lambda r: '🏠 Domicile' if r['winner_name'] == r['home_name'] else '✈️ Extérieur', axis=1)
        data = games['HomeWin'].value_counts().reset_index()

        data.columns = ['Resultat', 'Nombre']

        fig = px.pie(data, names='Resultat', values='Nombre', title=f"Avantage Terrain {season}", color_discrete_sequence=['#1e293b', '#94a3b8'], hole=0.4)
    else:
        teams_games = get_home_away_stats(team, season)

        if teams_games.empty: 
            return go.Figure(layout={"title": "Aucun match"})
        
        nickname = str(team).split()[-1].strip()

        wins = len(teams_games[teams_games['winner_name'].astype(str).str.contains(nickname, case=False, na=False)])
        losses = len(teams_games) - wins

        fig = px.pie(names=['Victoires', 'Défaites'], values=[wins, losses], title=f"Bilan : {team}", color_discrete_map={'Victoires': '#10b981', 'Défaites': '#ef4444'}, hole=0.4)
    
    fig.update_layout(legend_orientation="h", legend_y=-0.1, title_x=0.5)
    
    return fig

@callback(
    Output("finals-table", "data"),
    Input("team-dropdown", "value")
)
def update_finals_table(team):
    return get_finals_history(team).to_dict('records')

@callback(
    Output("finale-recap-container", "children"), 
    Input("season-dropdown", "value")
)
def update_finale_recap(season):
    finals = get_finals_summary(season)

    if finals.empty: 
        return html.H3("Données indisponibles")
    
    res = finals.iloc[0]

    if season == "ALL-TIME":
        season = "2018"
    
    return html.Div([
        html.H2(f"🏆 FINALE {season}", style={"color": "#fbbf24"}),
        html.P(f"{res['west_champion']} vs {res['east_champion']} | Score : {res['result']}"),
        html.H3(f"Champion : {res['champion']}")
    ])