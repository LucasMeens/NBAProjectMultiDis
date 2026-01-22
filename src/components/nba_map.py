from dash import dcc
import plotly.graph_objects as go

def nba_map_component(df_f, df_c, selected_team='ALL', options=None):
    if options is None: options = []
    fig = go.Figure()

    if 'density' in options:
        fig.add_trace(go.Densitymapbox(
            lat=df_c['lat'], lon=df_c['lng'], z=df_c['density'],
            radius=10, colorscale='Viridis', showscale=False, opacity=0.4
        ))

    dff = df_f.copy()
    if selected_team != 'ALL':
        dff = dff[dff['franchise'] == selected_team]

    fig.add_trace(go.Scattermapbox(
        lat=dff['lat'], lon=dff['lng'], mode='markers',
        marker=dict(size=12, color='red'),
        text=dff['franchise'], hoverinfo='text'
    ))

    fig.update_layout(
        mapbox=dict(style="carto-positron", center=dict(lat=37.09, lon=-95.71), zoom=3),
        margin={"r":0,"t":0,"l":0,"b":0}, height=500
    )
    return dcc.Graph(figure=fig)