import dash
from dash import html, dcc
from src.components.components.header import header

dash.register_page(__name__, path='/')

def layout():
    return html.Div(
        [
            html.Div(
                className="background-image"
            ),

            html.Div( 
                [
                    html.Div(
                        [ 
                            html.Div(
                                "PROJET MULTIDISCIPLINAIRE S1 2025-2026", 
                                className="project-box"
                            ),

                            html.H1(
                                "ANALYSE DES FRANCHISES NBA",
                                className="home-title"
                            ),

                            html.P(
                                "Une immersion dans les statistiques de la NBA. Densité de population, performance des joueurs et statistiques des franchises.", 
                                className="home-subtitle"
                            ),

                            html.Div(
                                [
                                    dcc.Link(
                                        "ALLER AUX GRAPHIQUES",
                                        href="/charts",
                                        className="home-button"
                                    ),
                                    dcc.Link(
                                        "RECHERCHER UN JOUEUR",
                                        href="/players",
                                        className="home-button"
                                    ),
                                    dcc.Link(
                                        "OÙ SONT LES FRANCHISES ?",
                                        href="/map",
                                        className="home-button",
                                    ),
                                ],
                                className="links-container"
                            )
                        ],
                        className="home-page"
                    )
                ],
                className="blue-wall"
            ),
        ]
    )