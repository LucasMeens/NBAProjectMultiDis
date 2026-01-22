import dash
from dash import Input, Output
from src.pages.dashboard import dashboard_layout
from src.components.nba_map import nba_map_component
from src.stats_service import load_all_data

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = dashboard_layout()

@app.callback(
    Output("map-container", "children"),
    [Input("team-dropdown", "value"), Input("map-options", "value")]
)
def update_map(team, opts):
    df_f, _, _, _, df_c = load_all_data()
    return nba_map_component(df_f, df_c, team, opts)

if __name__ == "__main__":
    app.run(debug=True, port=8050)