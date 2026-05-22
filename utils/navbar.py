"""
Navigation bar component for the dashboard.
"""

import dash_bootstrap_components as dbc

def create_navbar():
    """
    Create the top navigation bar for the dashboard.
    
    Returns:
        dbc.NavbarSimple: Navigation bar component
    """
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Overview", href="/", active="exact")),
            dbc.NavItem(dbc.NavLink("Customer Behavior", href="/behavior", active="exact")),
            dbc.NavItem(dbc.NavLink("Product Insights", href="/products", active="exact")),
            dbc.NavItem(dbc.NavLink("Correlations & Trends", href="/trends", active="exact")),
        ],
        brand="👗 Women's Clothing Reviews Dashboard",
        color="dark",
        dark=True,
        sticky="top",
    )
    return navbar
