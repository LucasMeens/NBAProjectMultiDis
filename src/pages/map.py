import dash
from dash import html
from src.components.components.header import *
from src.components.components.map_filter import *

dash.register_page(__name__, name="Carte Géographique")

_, seasons, options_teams = get_variables()

def layout():
    return html.Div(
    [
        header(),
        filter(seasons, options_teams),

        
        html.Div(
            [
                html.Div(
                    id="map-container", 
                    className="map-container",
                ),
            ],
            className="flex-box"
        ),
    ],
)
