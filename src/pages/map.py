import dash
from dash import html
from src.components.components.header import *
from src.components.components.filter import *
from src.components.components.team_cards import team_cards_component

dash.register_page(__name__)

_, seasons, options_teams = get_variables()

def layout():
    return html.Div(
    [
        header(),
        filter(seasons, options_teams),

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

        html.Div(id="map-container", style={"padding": "0 20px", "marginBottom": "30px"}),
    ]
)