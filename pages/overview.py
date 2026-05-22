"""
Overview page module.
Displays key metrics and dashboard overview charts.
"""

from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

def get_overview_layout(df):
    """
    Create the layout for the Overview page.
    
    Args:
        df: Processed dataframe
    
    Returns:
        dbc.Container: Page layout
    """
    overview_layout = dbc.Container([
        html.Br(),
        
        # KPI CARDS
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Reviews", className="card-title text-muted"),
                        html.H2(f"{len(df):,}", className="text-primary fw-bold")
                    ])
                ], className="h-100")
            ], md=6, lg=3, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Average Rating", className="card-title text-muted"),
                        html.H2(f"{df['Rating'].mean():.2f}/5", className="text-success fw-bold")
                    ])
                ], className="h-100")
            ], md=6, lg=3, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Recommended %", className="card-title text-muted"),
                        html.H2(f"{df['Recommended IND'].mean()*100:.1f}%", className="text-info fw-bold")
                    ])
                ], className="h-100")
            ], md=6, lg=3, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Avg Customer Age", className="card-title text-muted"),
                        html.H2(f"{df['Age'].mean():.1f}", className="text-warning fw-bold")
                    ])
                ], className="h-100")
            ], md=6, lg=3, className="mb-3"),
        ]),
        
        html.Hr(),
        
        # FILTERS
        dbc.Row([
            dbc.Col([
                html.H5("Filters", className="fw-bold mb-3")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Label("Department:", className="fw-bold"),
                dcc.Dropdown(
                    id='ov-department-dropdown',
                    options=[
                        {'label': 'All Departments', 'value': 'All'},
                        *[{'label': dep, 'value': dep} for dep in sorted(df['Department Name'].unique())]
                    ],
                    value='All',
                    clearable=False
                )
            ], md=4),
            
            dbc.Col([
                html.Label("Rating:", className="fw-bold"),
                dcc.RangeSlider(
                    id='ov-rating-slider',
                    min=1, max=5, step=0.5,
                    marks={i: str(i) for i in range(1, 6)},
                    value=[1, 5],
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], md=4),
        ], className="mb-4"),
        
        # CHARTS
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='ov-rating-dist')
            ], md=6),
            
            dbc.Col([
                dcc.Graph(id='ov-recommendation-line')
            ], md=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='ov-dept-bar')
            ]),
        ]),
        
    ], fluid=True)
    
    return overview_layout


def register_overview_callbacks(app, df):
    """
    Register all callbacks for the Overview page.
    
    Args:
        app: Dash application
        df: Processed dataframe
    """
    @app.callback(
        [Output('ov-rating-dist', 'figure'),
         Output('ov-recommendation-line', 'figure'),
         Output('ov-dept-bar', 'figure')],
        [Input('ov-department-dropdown', 'value'),
         Input('ov-rating-slider', 'value')]
    )
    def update_overview_charts(selected_dept, rating_range):
        # Filter data
        filtered_df = df.copy()
        if selected_dept != 'All':
            filtered_df = filtered_df[filtered_df['Department Name'] == selected_dept]
        filtered_df = filtered_df[(filtered_df['Rating'] >= rating_range[0]) & (filtered_df['Rating'] <= rating_range[1])]
        
        # Chart 1: Rating Distribution
        fig1 = px.histogram(
            filtered_df,
            x='Rating',
            nbins=5,
            title="Distribution of Customer Ratings",
            labels={'Rating': 'Rating', 'count': 'Number of Reviews'},
            color_discrete_sequence=['#636EFA']
        )
        fig1.update_layout(height=400, template='plotly_white', showlegend=False)
        
        # Chart 2: Recommendation by Rating
        rec_by_rating = filtered_df.groupby('Rating')['Recommended IND'].mean().reset_index()
        fig2 = px.line(
            rec_by_rating,
            x='Rating',
            y='Recommended IND',
            markers=True,
            title="Recommendation Probability by Rating",
            labels={'Recommended IND': 'Probability', 'Rating': 'Rating'},
            color_discrete_sequence=['#EF553B']
        )
        fig2.update_layout(height=400, template='plotly_white', showlegend=False)
        
        # Chart 3: Rating by Department (all departments)
        if selected_dept == 'All':
            dept_avg = df.groupby('Department Name')['Rating'].agg(['mean', 'count']).reset_index()
            fig3 = px.bar(
                dept_avg,
                x='Department Name',
                y='mean',
                title="Average Rating by Department",
                labels={'mean': 'Average Rating', 'Department Name': 'Department'},
                color_discrete_sequence=['#00CC96']
            )
        else:
            class_avg = filtered_df.groupby('Class Name')['Rating'].agg(['mean', 'count']).reset_index()
            fig3 = px.bar(
                class_avg,
                x='Class Name',
                y='mean',
                title=f"Average Rating by Class - {selected_dept}",
                labels={'mean': 'Average Rating', 'Class Name': 'Class'},
                color_discrete_sequence=['#AB63FA']
            )
        
        fig3.update_layout(height=400, template='plotly_white', showlegend=False)
        
        return fig1, fig2, fig3
