from dash import dcc, html

def charts_block():
    return html.Div([
        # --- Graphique 1 : Histogramme des Points ---
        html.Div([
            html.Div([
                dcc.Graph(
                    id="pts-hist",
                    config={'displayModeBar': False} # Masque la barre d'outils pour un look plus propre
                )
            ], style={
                "backgroundColor": "white", 
                "padding": "10px", 
                "borderRadius": "10px", 
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
            })
        ], style={"width": "32%", "display": "inline-block", "marginRight": "1%"}),
        
        # --- Graphique 2 : Analyse des Victoires ---
        html.Div([
            html.Div([
                dcc.Graph(
                    id="wins-hist",
                    config={'displayModeBar': False}
                )
            ], style={
                "backgroundColor": "white", 
                "padding": "10px", 
                "borderRadius": "10px", 
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
            })
        ], style={"width": "32%", "display": "inline-block", "marginRight": "1%"}),
        
        # --- Graphique 3 : Ratio Victoires/Défaites ---
        html.Div([
            html.Div([
                dcc.Graph(
                    id="ratio-pie",
                    config={'displayModeBar': False}
                )
            ], style={
                "backgroundColor": "white", 
                "padding": "10px", 
                "borderRadius": "10px", 
                "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
            })
        ], style={"width": "32%", "display": "inline-block"}),

    ], style={
        "display": "flex", 
        "justifyContent": "space-between", 
        "marginTop": "20px",
        "flexWrap": "wrap" # Permet de passer à la ligne sur petit écran
    })