import dash
from dash import html, dcc

def header():
    return html.Header(
        [
            html.Div(
                [
                    html.H1("NBA Analytics", style={"margin": 0, "fontSize": "24px"}),
                    html.P(
                        "Analyse complète des franchises NBA",
                        style={"margin": 0, "color": "#9ca3af", "fontSize": "12px"},
                    ),
                ],
                className="header-text"
            ),
            
            html.Nav(
                [
                    dcc.Link(
                        page["name"], 
                        href=page["relative_path"],
                        className="navigation-link"
                    ) for page in dash.page_registry.values()
                ],
                className="navigation"
            )
        ],
        className="header",
        style={"fontFamily": "sans-serif"}
    )
    