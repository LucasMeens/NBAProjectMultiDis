import dash
from dash import html, dcc, callback, Input, Output
from src.components.components.header import *

dash.register_page(__name__)

layout = html.Div([
    header(),

    html.Div([
            html.Div([
                html.Label("Franchise", style={"fontWeight": "bold", "color": "#1f2937"}),
                dcc.Dropdown(id="team-dropdown", options=options_teams, value="ALL", clearable=False, style={"marginBottom": "15px"}),
                html.Label("Saison", style={"fontWeight": "bold", "color": "#1f2937"}),
                dcc.Dropdown(id="season-dropdown", options=[{"label": str(s), "value": s} for s in seasons], value=seasons[0]),
                html.Label("Options Carte", style={"marginTop": "15px", "fontWeight": "bold", "display": "block"}),
                dcc.Checklist(id="map-options", options=[{"label": " Afficher densité population", "value": "density"}], value=[], style={"padding": "10px 0"}),
            ], style={"width": "28%", "display": "inline-block", "verticalAlign": "top", "padding": "20px", "backgroundColor": "white", "borderRadius": "12px", "boxShadow": "0 4px 6px -1px rgba(0,0,0,0.1)"}),
            
            html.Div([team_cards_component()], style={"width": "68%", "display": "inline-block", "marginLeft": "3%"}),
        ], style={"padding": "20px", "display": "flex", "alignItems": "stretch"}),

        html.Div(id="map-container", style={"padding": "0 20px", "marginBottom": "30px"}),
])