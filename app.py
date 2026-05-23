"""
Main entry point for the Women's Clothing Reviews Dashboard.

This app uses a modular structure with separate pages and utilities.
"""

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Import utilities and pages
from utils.data_loader import load_and_prepare_data
from utils.navbar import create_navbar
from pages.overview import get_overview_layout, register_overview_callbacks
from pages.behavior import get_behavior_layout, register_behavior_callbacks
from pages.products import get_products_layout, register_products_callbacks
from pages.trends import get_trends_layout, register_trends_callbacks

# ============================================
# LOAD & PREPARE DATA
# ============================================

df = load_and_prepare_data()

# ============================================
# INITIALIZE APP
# ============================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# ============================================
# CREATE PAGE LAYOUTS
# ============================================

navbar = create_navbar()

page_overview = get_overview_layout(df)
page_behavior = get_behavior_layout(df)
page_products = get_products_layout(df)
page_trends = get_trends_layout(df)

# ============================================
# MAIN APP LAYOUT
# ============================================

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
], fluid=True, style={"padding": "0px"})

# ============================================
# PAGE ROUTING CALLBACK
# ============================================

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to the appropriate page based on URL pathname."""
    if pathname == '/behavior':
        return page_behavior
    elif pathname == '/products':
        return page_products
    elif pathname == '/trends':
        return page_trends
    else:
        return page_overview

# ============================================
# REGISTER ALL CALLBACKS
# ============================================

register_overview_callbacks(app, df)
register_behavior_callbacks(app, df)
register_products_callbacks(app, df)
register_trends_callbacks(app, df)

# ============================================
# EXPORT SERVER FOR DEPLOYMENT
# ============================================

server = app.server

# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)