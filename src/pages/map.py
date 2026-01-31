import dash
from dash import html
from src.components.components.header import *
from src.components.components.map_filter import *

dash.register_page(__name__, name="Carte Géographique")

_, options_teams = get_variables()

def layout():
    return html.Div(
    [
        header(),
        filter(options_teams),

        
        html.Div(
            [
                html.Div(
                    id="map-container", 
                    className="map-container",
                ),
            ],
            className="flex-box"
        ),

        html.Div(
            [   
                html.Div(
                    [
                        html.H2(
                            "🏀 Le hasard n'a pas sa place sur le parquet.",
                            className="map-title"
                        ),
                        html.H3(
                            "Jetez un œil à cette carte : des parquets de Los Angeles aux neiges de Toronto, les 30 franchises NBA ne se sont pas installées là par chance. En superposant la localisation des équipes et la densité de population, une évidence saute aux yeux : la Grande Ligue suit la foule. Là où le cœur de l’Amérique bat le plus fort, la balle orange rebondit.",
                            className="map-text"
                        )
                    ]
                )
            ],
            className="flex-box"
        )
    ],
)
