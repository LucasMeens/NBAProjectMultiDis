from dash import Dash, dcc, html
from src.pages.dashboard import dashboard_layout
from src.pages.map import map_layout
from src.pages.players import players_layout

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("NBA Project MultiDisciplinaire", className="title"),

    dcc.Tabs([
        dcc.Tab(label="Dashboard", children=dashboard_layout()),
        dcc.Tab(label="Carte NBA", children=map_layout()),
        dcc.Tab(label="Joueurs", children=players_layout()),
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
