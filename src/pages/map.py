import pandas as pd
import numpy as np

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ImageURL
from bokeh.tile_providers import get_provider, OSM
from bokeh.util.geo import wgs84_to_web_mercator

output_notebook()

df = pd.read_csv("data/cleaned/franchises.csv")

df["logo"] = df["franchise"].apply(lambda x: f"assets/images/{x.split()[0]}.png")

df[["x", "y"]] = wgs84_to_web_mercator(df[["lng", "lat"]])

df["same_city_number"] = df.groupby(["lat", "lng"]).cumcount()

OFFSET = 3000  
df["x_jitter"] = df["x"] + df["same_city_number"] * OFFSET
df["y_jitter"] = df["y"] + df["same_city_number"] * OFFSET

source = ColumnDataSource(df)

p = figure(x_axis_type="mercator", y_axis_type="mercator", width=1000, height=700, title="NBA Franchises in the United States", tools="pan,wheel_zoom,box_zoom,reset")

p.add_tile(get_provider(OSM))

logos_map = ImageURL(url="logo", x="x_jitter", y="y_jitter", w=80000,  h=80000, anchor="center")

p.add_glyph(source, logos_map)

hover = HoverTool(tooltips=[("Franchise", "@franchise")])
p.add_tools(hover)

show(p)

