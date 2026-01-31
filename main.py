import dash
from dash import Input, Output, html
from src.components.components.nba_map import nba_map_component
from src.stats_service import load_map_data
from src.utils.clean_data import *
from src.utils.get_data import download

# download() # Remove the comments if you want to re-download and clean the CSV files
# clean()    # WARNING : It will takes longer to launch because of the downloading and cleaning

app = dash.Dash(__name__, use_pages=True, pages_folder="src/pages", suppress_callback_exceptions=True)
app.layout = html.Div(
    [
        dash.page_container
    ],
)

@app.callback(
    Output("map-container", "children"),
    [Input("team-dropdown", "value"), Input("map-options", "value")]
)
def update_map(team, opts):
    franchises, cities = load_map_data()
    return nba_map_component(franchises, cities, team, opts)

if __name__ == "__main__":

    app.run(debug=True, port=8050)