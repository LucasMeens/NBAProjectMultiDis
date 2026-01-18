from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

def nba_map_component(df_f, df_cities, selected_team, options):
    fig = go.Figure()

    if "density" in options and not df_cities.empty:
        fig.add_trace(go.Densitymapbox(
            lat=df_cities['lat'], lon=df_cities['lng'], z=df_cities['density'],
            radius=10, colorscale='Viridis', showscale=False, opacity=0.4
        ))

    if "logos" in options and not df_f.empty:
        dff = df_f.copy()
        
        # Gestion des doublons de coordonnées
        mask = dff.duplicated(subset=['lat', 'lng'], keep=False)
        dff.loc[mask, 'lat'] += np.random.uniform(-0.04, 0.04, size=mask.sum())
        dff.loc[mask, 'lng'] += np.random.uniform(-0.04, 0.04, size=mask.sum())

        if selected_team != "ALL":
            dff = dff[dff['franchise'] == selected_team]

        # On ajoute les points invisibles pour le hover text
        fig.add_trace(go.Scattermapbox(
            lat=dff['lat'], lon=dff['lng'],
            mode='markers',
            marker=dict(size=20, opacity=0), # Invisible mais capte le survol
            text=dff['franchise'],
            hoverinfo='text'
        ))

        # Ajout des logos via layout images
        for _, row in dff.iterrows():
            # Logique de nommage des fichiers
            city_name = str(row['city']).lower()
            franchise = str(row['franchise']).lower()
            
            img_name = f"{city_name}.png"
            if "clippers" in franchise: img_name = "losangeles1.png"
            elif "lakers" in franchise: img_name = "losangeles2.png"
            elif "brooklyn" in franchise or "nets" in franchise: img_name = "Brooklyn.png"

            fig.add_layout_image(
                dict(
                    source=f"/assets/images/{img_name}",
                    xref="x", yref="y",
                    x=row['lng'], y=row['lat'],
                    sizex=0.8, sizey=0.8, # Ajuste la taille selon tes besoins
                    xanchor="center", yanchor="middle"
                )
            )

    fig.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=38, lon=-95), zoom=3.5),
        margin={"r":0,"t":0,"l":0,"b":0}, height=600
    )
    return dcc.Graph(id='nba-main-map', figure=fig)