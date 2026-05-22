"""
Product Insights page module.
Displays product and department performance analytics.
"""

from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

def get_products_layout(df):
    """
    Create the layout for the Product Insights page.
    
    Args:
        df: Processed dataframe
    
    Returns:
        dbc.Container: Page layout
    """
    products_layout = dbc.Container([
        html.Br(),
        
        html.H3("Product & Department Insights", className="fw-bold mb-4"),
        
        # FILTERS
        dbc.Row([
            dbc.Col([
                html.Label("Department:", className="fw-bold"),
                dcc.Dropdown(
                    id='pd-department-dropdown',
                    options=[
                        {'label': dep, 'value': dep} for dep in sorted(df['Department Name'].unique())
                    ],
                    value=sorted(df['Department Name'].unique())[0],
                    clearable=False
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Top N Products:", className="fw-bold"),
                dcc.Slider(
                    id='pd-top-n-slider',
                    min=5, max=20, step=1,
                    marks={5: '5', 10: '10', 15: '15', 20: '20'},
                    value=10,
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], md=4),
        ], className="mb-4"),
        
        # CHARTS
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='pd-avg-by-dept')
            ], md=6),
            
            dbc.Col([
                dcc.Graph(id='pd-avg-by-class')
            ], md=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='pd-top-reviewed')
            ]),
        ]),
        
    ], fluid=True)
    
    return products_layout


def register_products_callbacks(app, df):
    """
    Register all callbacks for the Product Insights page.
    
    Args:
        app: Dash application
        df: Processed dataframe
    """
    @app.callback(
        [Output('pd-avg-by-dept', 'figure'),
         Output('pd-avg-by-class', 'figure'),
         Output('pd-top-reviewed', 'figure')],
        [Input('pd-department-dropdown', 'value'),
         Input('pd-top-n-slider', 'value')]
    )
    def update_products_charts(selected_dept, top_n):
        # Filter data
        filtered_df = df[df['Department Name'] == selected_dept]
        
        # Chart 1: Avg Rating by Department
        dept_avg = df.groupby('Department Name')['Rating'].mean().reset_index().sort_values('Rating', ascending=False)
        fig1 = px.bar(
            dept_avg,
            x='Department Name',
            y='Rating',
            title="Average Rating by Department",
            labels={'Rating': 'Average Rating', 'Department Name': 'Department'},
            color_discrete_sequence=['#636EFA']
        )
        fig1.update_layout(height=400, template='plotly_white', showlegend=False)
        
        # Chart 2: Avg Rating by Class Name
        class_avg = df.groupby('Class Name')['Rating'].mean().reset_index().sort_values('Rating', ascending=False)
        fig2 = px.bar(
            class_avg,
            x='Class Name',
            y='Rating',
            title="Average Rating by Class Name",
            labels={'Rating': 'Average Rating', 'Class Name': 'Class'},
            color_discrete_sequence=['#EF553B']
        )
        fig2.update_layout(height=400, template='plotly_white', showlegend=False)
        
        # Chart 3: Top Reviewed Products in Selected Department
        top_products = filtered_df.groupby('Clothing ID').size().reset_index(name='Review Count').nlargest(top_n, 'Review Count')
        top_products = top_products.merge(
            filtered_df.groupby('Clothing ID')['Rating'].mean().reset_index(),
            on='Clothing ID'
        )
        top_products['Clothing ID'] = 'ID ' + top_products['Clothing ID'].astype(str)
        
        fig3 = px.bar(
            top_products,
            x='Clothing ID',
            y='Review Count',
            color='Rating',
            title=f"Top {top_n} Most Reviewed Items - {selected_dept}",
            labels={'Review Count': 'Number of Reviews', 'Clothing ID': 'Product ID', 'Rating': 'Avg Rating'},
            color_continuous_scale='RdYlGn',
            range_color=[1, 5]
        )
        fig3.update_layout(height=400, template='plotly_white')
        
        return fig1, fig2, fig3
