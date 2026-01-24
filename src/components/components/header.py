import dash
from dash import html, dcc

def header():
    return html.Div(
        [
            html.H1("NBA Analytics Dashboard", style={"margin": 0, "letterSpacing": "1px"}),
            html.P(
                "Analyse complète : Franchises, Densité Urbaine, Performances et Palmarès.",
                style={"marginTop": 5, "color": "#9ca3af", "fontSize": "14px"},
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Link(f"{page['name']}", href=page["relative_path"]) 
                    )for page in dash.page_registry.values()
                ]
            ) 
        ],
        style={
            "padding": "20px 30px",
            "backgroundColor": "#111827", # Noir profond
            "color": "white",
            "borderBottom": "2px solid #1d4ed8", # Ligne bleue NBA
            "fontFamily": "sans-serif"
        },
    )