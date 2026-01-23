import pandas as pd
import numpy as np

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ImageURL
from bokeh.tile_providers import get_provider, OSM
from bokeh.util.geo import wgs84_to_web_mercator

output_notebook()

franchises = pd.read_csv("data/cleaned/franchises.csv")

franchises["logo"] = franchises["franchise"].apply(lambda x: f"assets/images/{x.split()[0]}.png")

franchises[["x", "y"]] = wgs84_to_web_mercator(franchises[["lng", "lat"]])

franchises["same_city_number"] = franchises.groupby(["lat", "lng"]).cumcount()

OFFSET = 3000  
franchises["x_jitter"] = franchises["x"] + franchises["same_city_number"] * OFFSET
franchises["y_jitter"] = franchises["y"] + franchises["same_city_number"] * OFFSET

source = ColumnDataSource(franchises)

map = figure(x_axis_type="mercator", y_axis_type="mercator", width=1000, height=700, title="NBA Franchises in the United States", tools="pan,wheel_zoom,box_zoom,reset")

map.add_tile(get_provider(OSM))

logos_map = ImageURL(url="logo", x="x_jitter", y="y_jitter", w=80000,  h=80000, anchor="center")

map.add_glyph(source, logos_map)

hover = HoverTool(tooltips=[("Franchise", "@franchise")])
map.add_tools(hover)

show(p)

