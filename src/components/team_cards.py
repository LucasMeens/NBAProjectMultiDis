from dash import html

def team_cards_component():
    return html.Div(
        [
            html.H3("Informations sur la franchise", style={"marginBottom": "20px"}),
            html.Div(
                id="team-cards-container",
                style={"display": "flex", "gap": "20px", "flexWrap": "wrap"},
            ),
        ],
        style={"marginTop": 20},
    )

def _info_card(title, value, subtitle):
    return html.Div(
        [
            html.Div(title, style={"fontSize": "14px", "color": "#6b7280"}),
            html.Div(value, style={"fontSize": "24px", "fontWeight": "bold"}),
            html.Div(subtitle, style={"fontSize": "12px", "color": "#9ca3af"}),
        ],
        style={
            "padding": "15px 20px",
            "border": "1px solid #e5e7eb",
            "borderRadius": "8px",
            "minWidth": "180px",
            "backgroundColor": "white",
            "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
        },
    )