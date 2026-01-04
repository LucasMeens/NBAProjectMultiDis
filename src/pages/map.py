from dash import html, dcc
import plotly.express as px
from src.backend.stats_service import (
    get_points_distribution,
    get_top_players,
    get_boxplot_by_position,
    get_scatter_points_vs_shots
)

def dashboard_layout():
    df_points = get_points_distribution()
    fig_hist = px.histogram(
        df_points,
        x="Points",
        color="Team",
        title="Distribution des points par joueur"
    )

    top5 = get_top_players("Points")
    fig_top5 = px.bar(
        top5,
        x="Points",
        y="Player",
        orientation="h",
        title="Top 5 joueurs par points"
    )

    box_df = get_boxplot_by_position()
    fig_box = px.box(
        box_df,
        x="Position",
        y="Points",
        title="Performance par position"
    )

    scatter_df = get_scatter_points_vs_shots()
    fig_scatter = px.scatter(
        scatter_df,
        x="FGA",
        y="Points",
        color="Team",
        title="Corrélation tirs tentés / points"
    )

    return html.Div([
        dcc.Graph(figure=fig_hist),
        dcc.Graph(figure=fig_top5),
        dcc.Graph(figure=fig_box),
        dcc.Graph(figure=fig_scatter),
    ])
