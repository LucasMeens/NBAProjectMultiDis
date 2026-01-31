from dash import dcc
import plotly.graph_objects as go
import numpy as np

def nba_map_component(franchises, cities, selected_team, options):
    
    fig = go.Figure()

    options = options if options is not None else []

    if "density" in options and cities is not None and not cities.empty:

        fig.add_trace(
            go.Densitymapbox(
                lat=cities['lat'], 
                lon=cities['lng'], 
                z=cities['density'],
                
                radius=12, 
                colorscale='Viridis', 
                showscale=False, 
                opacity=0.5,
                name="Densité"
            )
        )

    if franchises is not None and not franchises.empty:
        franchises_copy = franchises.copy()
        
        mask = franchises_copy.duplicated(subset=['lat', 'lng'], keep=False)
        
        if mask.any():
            franchises_copy.loc[mask, 'lat'] += np.random.uniform(-0.05, 0.05, size=mask.sum())
            franchises_copy.loc[mask, 'lng'] += np.random.uniform(-0.05, 0.05, size=mask.sum())

        if selected_team != "ALL":
            franchises_copy = franchises_copy[franchises_copy['franchise'] == selected_team]

        fig.add_trace(go.Scattermapbox(
            lat=franchises_copy['lat'], 
            lon=franchises_copy['lng'],

            mode='markers+text',
            marker=dict(
                size=14, 
                color='#ef4444', 
                opacity=0.9
            ),
            
            text=franchises_copy['franchise'] if selected_team == "ALL" else "",
            textposition="top center",
            hoverinfo='text'
        ))


    center = {"lat": 38.0, "lon": -95.0}
    zoom = 3.5

    if selected_team != "ALL" and not franchises_copy.empty:
        center = {"lat": franchises_copy['lat'].iloc[0], "lon": franchises_copy['lng'].iloc[0]}
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