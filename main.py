import dash
from dash import html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned")

df_f = pd.read_csv(os.path.join(DATA_PATH, 'franchises.csv'))
df_c = pd.read_csv(os.path.join(DATA_PATH, 'cities.csv'))
df_g = pd.read_csv(os.path.join(DATA_PATH, 'games.csv'))
df_p = pd.read_csv(os.path.join(DATA_PATH, 'players_stats.csv'))
df_w = pd.read_csv(os.path.join(DATA_PATH, 'wins.csv'))

from src.components.header import header
from src.components.nba_map import nba_map_component
from src.components.team_cards import team_cards_component, _info_card
from src.components.charts import charts_block

app = dash.Dash(__name__, title="NBA Analytics")

app.layout = html.Div([
    header(),
    
    html.Div([
        dcc.Dropdown(
            id='team-selector',
            options=[{'label': '🏀 Toutes les franchises', 'value': 'ALL'}] + 
                    [{'label': t, 'value': t} for t in sorted(df_f['franchise'].unique())],
            value='ALL',
            clearable=False,
            style={"width": "400px"}
        ),
    ], style={"padding": "20px"}),

    html.Div([
        dcc.Checklist(
            id='map-layers',
            options=[{'label': ' Densité Population', 'value': 'density'}, 
                     {'label': ' Logos Teams', 'value': 'logos'}],
            value=['logos'], inline=True, style={"padding": "0 20px 10px 20px"}
        ),
        html.Div(id='map-wrapper')
    ]),

    team_cards_component(),
    charts_block(),

    html.Div(id="finale-summary", style={
        "marginTop": "40px", "padding": "40px", "backgroundColor": "#f8f9fa",
        "borderTop": "3px solid #111827", "textAlign": "center"
    })
])

@app.callback(
    [Output('map-wrapper', 'children'),
     Output('team-cards-container', 'children'),
     Output('pts-hist', 'figure'),
     Output('wins-hist', 'figure'),
     Output('ratio-pie', 'figure'),
     Output('finals-table', 'data'),
     Output('player-stats-table', 'data'),
     Output('finale-summary', 'children')],
    [Input('team-selector', 'value'),
     Input('map-layers', 'value'),
     Input('player-search-input', 'value')]
)
def global_update(team, layers, player_search):
    map_fig = nba_map_component(df_f, df_c, team, layers)

    titles = len(df_w[df_w['champion'] == team]) if team != "ALL" else 0
    cards = [_info_card("Titres NBA", str(titles), "Historique")]

    fig_pts = px.bar(df_p.groupby('season')['points_per_game'].mean().reset_index(), 
                     x='season', y='points_per_game', title="PPG Moyen par Saison (NBA)")
    
    fig_wins = px.histogram(df_g.head(50), x="winner_name", title="Performance Victoires")
    fig_pie = px.pie(values=[65, 35], names=['V', 'D'], hole=0.4, title="Ratio Victoire")

    f_data = df_w.to_dict('records')
    p_data = df_p[df_p['player'].str.contains(player_search, case=False, na=False)].head(15).to_dict('records')

    last_win = df_w.iloc[-1]
    hist_titles = len(df_w[df_w['champion'] == last_win['champion']])
    footer = html.Div([
        html.H2("🏆 Résumé de la finale NBA"),
        html.P(f"L'équipe des {last_win['champion']} s'est imposée ({last_win['result']}).", style={"fontSize": "20px"}),
        html.P(f"C'est leur {hist_titles}ème titre NBA.")
    ])

    return map_fig, cards, fig_pts, fig_wins, fig_pie, f_data, p_data, footer

if __name__ == "__main__":
    app.run(debug=True)