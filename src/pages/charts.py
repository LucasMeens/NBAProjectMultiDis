import dash
from dash import html, dcc, callback, Input, Output, dash_table
from src.components.components.charts_filter import get_variables, filter
from src.components.components.header import header
from src.stats_service import *
import plotly.express as px
import plotly.graph_objects as go
from src.components.components.team_cards import team_cards_component

dash.register_page(__name__, name="Analyse Statistique")

teams, seasons, options_teams = get_variables()

def layout():
    return html.Div(
    [
        header(),
        
        
        html.Div(
            [
                html.Div(
                    [
                        filter(seasons, options_teams),

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
    raw = get_points_per_game(team, season) #Les données brutes qui proviennent de stats_service.py
    if raw is None or raw.empty:
        return go.Figure().update_layout(title=f"Aucun match trouvé pour {team}")
    
    df = pd.DataFrame(raw.to_dict())

    if str(season) == "ALL-TIME":
        df['Decade'] = (df['year'] // 10 * 10).astype(str) + "s"
        fig = px.histogram(
            df, x="score_obtenu", color="Decade", marginal="box",
            title=f"Puissance offensive : {team} (Par Décennie)",
            labels={'score_obtenu': 'Points marqués', 'Decade': 'Époque'},
            barmode='overlay', opacity=0.6,
            template="plotly_white"
        )
    else:
        fig = px.histogram(
            df, x="score_obtenu", nbins=15,
            title=f"Puissance Offensive : {team} ({season})",
            labels={'score_obtenu': 'Points marqués'},
            color_discrete_sequence=['#3b82f6'],
            template="plotly_white" 
        )

    fig.add_vline(x=100, line_dash="dash", line_color="grey")
    fig.add_vline(x=120, line_dash="dash", line_color="grey")
    fig.update_layout(bargap=0.1, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_x=0.5)
    return fig


@callback(
    Output("wins-hist", "figure"), 
    [
        Input("team-dropdown", "value"), 
        Input("season-dropdown", "value")
    ]
)
def update_wins_analysis(team, season):
    raw = get_home_away_stats(team, season)
    
    if raw is None or (isinstance(raw, pd.DataFrame) and raw.empty):
        return go.Figure().update_layout(title="Aucune donnée disponible")

    plot = pd.DataFrame(raw)
    lab_home, lab_away = "🏠 Domicile", "✈️ Extérieur"
    
    if team == "ALL":
        plot['Lieu'] = plot.apply(
            lambda r: lab_home if r['home_score'] > r['away_score'] else lab_away, axis=1
        )
    else:
        team_selected = str(team).strip().lower()
        
        def get_loc(row):
            winner = str(row.get('winner_name', '')).strip().lower()
            home = str(row.get('home_name', '')).strip().lower()
            if winner in team_selected or team_selected.split()[-1] == winner:
                return lab_home if (home in team_selected or team_selected.split()[-1] == home) else lab_away
            return None

        plot['Lieu'] = plot.apply(get_loc, axis=1) #plot fait ici référence à Plotly c'est le DataFrame spécifiquement préparé pour
        plot = plot[plot['Lieu'].notna()]

    if plot.empty:
        return go.Figure().update_layout(title=f"Pas de victoires pour {team}")

    wins_split = plot.groupby(['year', 'Lieu']).size().reset_index(name='Total') #Divise le total de victoires en deux catégories visuelles (Domicile vs Extérieur) pour chaque année

    fig = px.bar(
        wins_split, 
        x='year', 
        y='Total', 
        color='Lieu',
        title=f"Victoires : {team}", 
        barmode='group',
        color_discrete_map={lab_home: "#065f46", lab_away: "#ef4444"},
        template="plotly_white" # Utilise un template standard explicite
    )
    fig.update_traces(marker_pattern_shape="") # Patch 3.13 (car on avait eu un bug lors du lancement à ce niveau là)
    return fig

@callback(
    Output("ratio-pie", "figure"), 
    [
        Input("team-dropdown", "value"), 
        Input("season-dropdown", "value")
    ]
)
def update_ratio_logic(team, season):
    raw_df = get_home_away_stats(team, season)
    if raw_df is None or raw_df.empty: 
        return go.Figure(layout={"title": "Aucun match"})

    df = pd.DataFrame(raw_df.to_dict())

    if team == "ALL":
        
        df['diff'] = abs(df['home_score'] - df['away_score'])
        def cat_game(d): #Permet de créer une classification ds matchs à partir de l'écart de points
            if d <= 5: return "🔥 Match Serrés (<=5 pts)"
            if d >= 15: return "🧊 Démonstration (>=15 pts)"
            return "🏀 Match Standards"
        df['Type'] = df['diff'].apply(cat_game)
        data = df['Type'].value_counts().reset_index()
        fig = px.pie(data, names='Type', values='count', hole=0.4,
                     title=f"Intensité des matchs NBA ({season})",
                     color_discrete_map={"🔥 Match Serrés (<=5 pts)": "#ef4444", "🏀 Match Standards": "#3b82f6", "🧊 Démonstration de force (>=15 pts)": "#94a3b8"})
    else:

        keywords_map = {"Oklahoma City": ["Thunder", "Sonics", "Seattle"], "New Orleans Pelicans": ["Pelicans", "Hornets", "New Orleans"], "Los Angeles Clippers": ["Clippers", "San Diego", "Buffalo"], "Brooklyn Nets": ["Nets", "New Jersey"]}
        words = keywords_map.get(team, [str(team).split()[-1].strip()])
        def check_win(r):
            is_home = any(w.lower() in str(r['home_name']).lower() for w in words)
            return (is_home and r['home_score'] > r['away_score']) or (not is_home and r['away_score'] > r['home_score'])
        df['won'] = df.apply(check_win, axis=1)
        v, d = df['won'].sum(), len(df) - df['won'].sum()
        fig = px.pie(names=['Victoires', 'Défaites'], values=[v, d], hole=0.4,
                     title=f"Bilan : {team}", color_discrete_map={'Victoires': '#10b981', 'Défaites': '#ef4444'})

    fig.update_layout(legend_orientation="h", legend_y=-0.1, title_x=0.5, paper_bgcolor='rgba(0,0,0,0)')
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