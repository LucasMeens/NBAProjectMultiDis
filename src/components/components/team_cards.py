from dash import html, Output, Input, callback

def team_logo_card(team_name):
    
    if not team_name:
        return html.Div()

    name = str(team_name).lower().strip()
    
    # On utilise un dictionnaire de mapping pour une sélection directe et sans erreur
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

    # On cherche d'abord dans le dictionnaire, sinon on prend le premier mot
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
            style={"height": "80px", "width": "auto", "objectFit": "contain"},
            alt=f"Logo {team_name}"
        ),
        style={
            "padding": "10px 20px", 
            "backgroundColor": "white", 
            "borderRadius": "12px", 
            "border": "1px solid #e5e7eb",
            "display": "flex", 
            "alignItems": "center",
            "justifyContent": "center", 
            "minWidth": "140px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"
        }
    )

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

@callback(
    Output("team-cards-container", "children"),
    [Input("team-dropdown", "value"), 
     Input("season-dropdown", "value")]
)
def update_team_info_cards(team, season):
    
    if team == "ALL":
        return [
            _info_card("Ligue", "NBA", "30 Franchises"),
            _info_card("Saison", str(season), "Vue globale")
        ]
    
    # C'est ici qu'on affiche le logo et les infos de l'équipe sélectionnée car sur la map ça empêchait d'avoir l'option densité
    return [
        team_logo_card(team),
        _info_card("Franchise", team, "Sélectionnée"),
        _info_card("Saison", str(season), "Filtre actif")
    ]
