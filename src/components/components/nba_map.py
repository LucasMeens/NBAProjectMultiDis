from dash import dcc
import plotly.graph_objects as go
import numpy as np

def nba_map_component(df_f, df_cities, selected_team, options):
    
    fig = go.Figure()
    options = options if options is not None else []

    # 1. COUCHE DENSITÉ (Heatmap)

    if "density" in options and df_cities is not None and not df_cities.empty:
        fig.add_trace(go.Densitymapbox(
            lat=df_cities['lat'], 
            lon=df_cities['lng'], 
            z=df_cities['density'],
            radius=12, 
            colorscale='Viridis', 
            showscale=False, 
            opacity=0.5,
            name="Densité"
        ))

    # 2. COUCHE FRANCHISES (Finalement j'ai décidé de procéder avec Points)
    if df_f is not None and not df_f.empty:
        dff = df_f.copy()
        
        # Micro-décalage pour les coordonnées identiques (Lakers/Clippers et Knicks/Nets)
        mask = dff.duplicated(subset=['lat', 'lng'], keep=False)
        if mask.any():
            dff.loc[mask, 'lat'] += np.random.uniform(-0.05, 0.05, size=mask.sum())
            dff.loc[mask, 'lng'] += np.random.uniform(-0.05, 0.05, size=mask.sum())

        # Filtrage par équipe
        if selected_team != "ALL":
            dff = dff[dff['franchise'] == selected_team]

        # Ajout des points sur la carte
        fig.add_trace(go.Scattermapbox(
            lat=dff['lat'], 
            lon=dff['lng'],
            mode='markers+text',
            marker=dict(
                size=14, 
                color='#ef4444', 
                opacity=0.9
            ),
            # On affiche le nom uniquement si "ALL" est sélectionné
            text=dff['franchise'] if selected_team == "ALL" else "",
            textposition="top center",
            hoverinfo='text'
        ))

    # 3. CONFIGURATION DU LAYOUT
    # Avec un zoom par défaut sur les Etats Unis 

    center = {"lat": 38.0, "lon": -95.0}
    zoom = 3.5

    # Là du coup on zoom sur la franchise sélectionné
    if selected_team != "ALL" and not dff.empty:
        center = {"lat": dff['lat'].iloc[0], "lon": dff['lng'].iloc[0]}
        zoom = 5

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=center,
            zoom=zoom
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=550
    )

    return dcc.Graph(id='nba-main-map', figure=fig)