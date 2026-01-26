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
                                        "display": "inline-block", 
                                        "marginLeft": "3%"
                                    }
                                ),
                            ], 
                            style={
                                "padding": "20px", 
                                "display": "flex", 
                                "alignItems": "stretch"
                            }
                        ),

                        html.Div(
                            [ 
                                # ---------------------------------------
                                # First Graph : Points histogram
                                # ---------------------------------------
                                html.Div([
                                    html.Div([
                                        dcc.Graph(
                                            id="pts-hist",
                                            config={'displayModeBar': False} # Masque la barre d'outils pour un look plus propre
                                        )
                                    ], style={
                                        "backgroundColor": "white", 
                                        "borderRadius": "10px", 
                                        "paddingRight" : "10px",
                                        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
                                    })
                                ], style={"width": "32%", "display": "inline-block", "marginRight": "1%"}),
                                
                                # ---------------------------------------
                                # Second Graph : Victory analysis
                                # ---------------------------------------
                                html.Div([
                                    html.Div([
                                        dcc.Graph(
                                            id="wins-hist",
                                            config={'displayModeBar': False},
                                        )
                                    ], style={
                                        "backgroundColor": "white", 
                                        "paddingRight" : "10px",
                                        "borderRadius": "10px", 
                                        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
                                    })
                                ], style={"width": "32%", "display": "inline-block", "marginRight": "1%"}),
                                
                                # ---------------------------------------
                                # Third Graph : Wins/Lose Ratio
                                # ---------------------------------------        
                                html.Div([
                                    html.Div([
                                        dcc.Graph(
                                            id="ratio-pie",
                                            config={'displayModeBar': False}
                                        )
                                    ], style={
                                        "backgroundColor": "white", 
                                        "paddingRight" : "10px",
                                        "borderRadius": "10px", 
                                        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
                                    })
                                ], style={"width": "32%", "display": "inline-block"}),

                            ], 
                            style={
                                "display": "flex", 
                                "justifyContent": "space-between", 
                                "marginTop": "20px",
                                "flexWrap": "wrap" # Permet de passer à la ligne sur petit écran
                            }
                        ),

                        html.Div(
                            [
                                html.H3(
                                    "📜 Historique des Finales NBA", 
                                    style={
                                        "marginTop": "40px", 
                                        "color": "#1f2937"
                                    }
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
                            style={
                                "margin": "40px 0px", 
                                "padding": "30px", 
                                "backgroundColor": "#111827", 
                                "color": "white", 
                                "borderRadius": "15px", 
                                "textAlign": "center"
                            }
                        ), 
                    ],
                    style={
                        "width" : "80%"
                    }
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
    df = get_points_per_game(team, season)
    
    if df.empty:
        return go.Figure().update_layout(title="Aucune donnée trouvée")

    title = f"Points/Match : {team} ({season})"
    fig = px.histogram(df, x="points_per_game", nbins=20 if season == "ALL-TIME" else 10, 
                       title=title, color_discrete_sequence=['#3b82f6'],
                       hover_data=["player", "season"])
    
    fig.update_layout(bargap=0.1, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

@callback(Output("wins-hist", "figure"), [Input("team-dropdown", "value"), Input("season-dropdown", "value")])
def update_wins_analysis(team, season):
    df_all_games = get_home_away_stats("ALL", season)
    if team == "ALL":
        counts = df_all_games['winner_name'].value_counts().nlargest(10).reset_index()
        counts.columns = ['Equipe', 'Victoires']
        fig = px.bar(counts, x='Equipe', y='Victoires', title="Top 10 Victoires", color='Victoires', color_continuous_scale='Blues')
    else:
        nickname = str(team).split()[-1].strip()
        df_team_wins = df_all_games[df_all_games['winner_name'].astype(str).str.contains(nickname, case=False, na=False)].copy()

        if df_team_wins.empty: 
            return go.Figure(layout={"title": f"0 victoires pour {nickname}"})
        
        df_team_wins['Lieu'] = df_team_wins.apply(lambda r: '🏠 Domicile' if nickname.lower() in str(r['home_name']).lower() else '✈️ Extérieur', axis=1)
        
        data = df_team_wins['Lieu'].value_counts().reset_index()
        data.columns = ['Lieu', 'Victoires']
        
        fig = px.bar(data, x='Lieu', y='Victoires', title=f"Victoires : {team}", color='Lieu', color_discrete_map={'🏠 Domicile': '#1d4ed8', '✈️ Extérieur': '#60a5fa'})
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_x=0.5)
    
    return fig

@callback(Output("ratio-pie", "figure"), [Input("team-dropdown", "value"), Input("season-dropdown", "value")])
def update_ratio_logic(team, season):
    if team == "ALL":
        df_games = get_home_away_stats("ALL", season)
        df_games['HomeWin'] = df_games.apply(lambda r: '🏠 Domicile' if r['winner_name'] == r['home_name'] else '✈️ Extérieur', axis=1)
        data = df_games['HomeWin'].value_counts().reset_index()
        data.columns = ['Resultat', 'Nombre']
        fig = px.pie(data, names='Resultat', values='Nombre', title=f"Avantage Terrain {season}", color_discrete_sequence=['#1e293b', '#94a3b8'], hole=0.4)
    else:
        df_team_matches = get_home_away_stats(team, season)
        if df_team_matches.empty: return go.Figure(layout={"title": "Aucun match"})
        nickname = str(team).split()[-1].strip()
        wins = len(df_team_matches[df_team_matches['winner_name'].astype(str).str.contains(nickname, case=False, na=False)])
        losses = len(df_team_matches) - wins
        fig = px.pie(names=['Victoires', 'Défaites'], values=[wins, losses], title=f"Bilan : {team}", color_discrete_map={'Victoires': '#10b981', 'Défaites': '#ef4444'}, hole=0.4)
    fig.update_layout(legend_orientation="h", legend_y=-0.1, title_x=0.5)
    return fig

@callback(Output("finals-table", "data"), Input("team-dropdown", "value"))
def update_finals_table(team):
    return get_finals_history(team).to_dict('records')

@callback(Output("finale-recap-container", "children"), Input("season-dropdown", "value"))
def update_finale_recap(season):
    df = get_finals_summary(season)
    if df.empty: return html.H3("Données indisponibles")
    res = df.iloc[0]
    return html.Div([
        html.H2(f"🏆 RÉCAPITULATIF FINALE {season}", style={"color": "#fbbf24"}),
        html.P(f"{res['west_champion']} vs {res['east_champion']} | Score : {res['result']}"),
        html.H3(f"Champion : {res['champion']}")
    ])