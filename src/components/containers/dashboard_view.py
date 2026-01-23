from dash import html, dcc, callback, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from src.stats_service import *
from src.components.components.header import header
from src.components.components.charts import charts_block
from src.components.components.team_cards import team_cards_component
from src.components.components.filter import filter
from src.stats_service import get_team_list, get_season_list

def dashboard_layout():
    teams = get_team_list()
    seasons = get_season_list()
    options_teams = [{"label": "🏀 Toutes les franchises", "value": "ALL"}] + [{"label": t, "value": t} for t in teams]


    return html.Div([
        header(),
        
        html.Div([
                html.Label("Franchise", style={"fontWeight": "bold", "color": "#1f2937"}),
                dcc.Dropdown(id="team-dropdown", options=options_teams, value="ALL", clearable=False, style={"marginBottom": "15px"}),
                html.Label("Saison", style={"fontWeight": "bold", "color": "#1f2937"}),
                dcc.Dropdown(id="season-dropdown", options=[{"label": str(s), "value": s} for s in seasons], value=seasons[0]),
                html.Label("Options Carte", style={"marginTop": "15px", "fontWeight": "bold", "display": "block"}),
                dcc.Checklist(id="map-options", options=[{"label": " Afficher densité population", "value": "density"}], value=[], style={"padding": "10px 0"}),
        ], style={"width": "28%", "display": "inline-block", "verticalAlign": "top", "padding": "20px", "backgroundColor": "white", "borderRadius": "12px", "boxShadow": "0 4px 6px -1px rgba(0,0,0,0.1)"}),

        html.Div([charts_block()], style={"padding": "0 20px"}),

        html.Div([
            html.H3("📜 Historique des Finales NBA", style={"marginTop": "40px", "color": "#1f2937"}),
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
                style_cell={'textAlign': 'center', 'padding': '10px', 'fontFamily': 'sans-serif'},
                page_size=10
            )
        ], style={"padding": "20px"}),

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

        html.Div(id="finale-recap-container", style={
            "margin": "40px 20px", "padding": "30px", "backgroundColor": "#111827", 
            "color": "white", "borderRadius": "15px", "textAlign": "center"
        })
    ], style={"backgroundColor": "#f9fafb", "minHeight": "100vh", "fontFamily": "sans-serif"})


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

@callback(Output("player-stats-table", "data"), Input("player-search-input", "value"))
def update_player_table(search_value):
    if not search_value: return []
    return get_player_stats(search_value).to_dict('records')

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