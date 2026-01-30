from dash import html, Output, Input, callback

def team_logo_card(team_name):
    
    if not team_name:
        return html.Div()

    name = str(team_name).lower().strip()
    
    mapping = {
        "hornets": "charlotte.png",
        "charlotte": "charlotte.png",
        "knicks": "newyork.png",
        "nets": "brooklyn.png",
        "brooklyn": "brooklyn.png",
        "clippers": "losangeles1.png",
        "lakers": "losangeles2.png",
        "warriors": "sanfrancisco.png",
        "kings": "sacramento.png",
        "thunder": "oklahomacity.png",
        "okc": "oklahomacity.png",
        "pelicans": "neworleans.png",
        "spurs": "sanantonio.png"
    }

    filename = None
    for key in mapping:
        if key in name:
            filename = mapping[key]
            break
    
    if not filename:
        filename = f"{name.split()[0]}.png"

    return html.Div(
        html.Img(
            src=f"/assets/images/{filename}", 
            className="team-logo",
            alt=f"Logo {team_name}"
        ),
        className="team-logo-container"
    )

def info_card(title, value, subtitle):
    return html.Div(
        [
            html.Div(title, style={"fontSize": "14px", "color": "#6b7280"}),
            html.Div(value, style={"fontSize": "24px", "fontWeight": "bold"}),
            html.Div(subtitle, style={"fontSize": "12px", "color": "#9ca3af"}),
        ],
        className="team-logo-card"
    )

def team_cards_component():
    return html.Div(
        [
            html.H2(
                "ℹ️ Informations sur la franchise", 
                className="charts-title"
            ),
            html.Div(
                id="team-cards-container",
                className="info-bubbles"
            ),
        ],
    )

@callback(
    Output("team-cards-container", "children"),
    [
        Input("team-dropdown", "value"), 
        Input("season-dropdown", "value")
    ]
)
def update_team_info_cards(team, season):
    
    if team == "ALL":
        return [
            info_card("Ligue", "NBA", "30 Franchises"),
            info_card("Saison", str(season), "Vue globale")
        ]

    return [
        team_logo_card(team),
        info_card("Franchise", team, "Sélectionnée"),
        info_card("Saison", str(season), "Filtre actif")
    ]
