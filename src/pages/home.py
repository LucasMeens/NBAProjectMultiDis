import dash
from dash import html
from src.components.components.header import header

dash.register_page(__name__, path='/')

def layout():
    return html.Div(
    [
        header(),

        html.H1('Home page'),
        html.P('In progress...')
    ]
)