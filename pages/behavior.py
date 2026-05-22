"""
Customer Behavior page module.
Analyzes customer behavior patterns and metrics.
"""

from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

def get_behavior_layout(df):
    """
    Create the layout for the Customer Behavior page.
    
    Args:
        df: Processed dataframe
    
    Returns:
        dbc.Container: Page layout
    """
    behavior_layout = dbc.Container([
        html.Br(),
        
        html.H3("Customer Behavior Analysis", className="fw-bold mb-4"),
        
        # FILTERS
        dbc.Row([
            dbc.Col([
                html.Label("Clothing Class:", className="fw-bold"),
                dcc.Dropdown(
                    id='bh-class-dropdown',
                    options=[
                        {'label': 'All Classes', 'value': 'All'},
                        *[{'label': cls, 'value': cls} for cls in sorted(df['Class Name'].unique())]
                    ],
                    value='All',
                    clearable=False
                )
            ], md=6),
            
            dbc.Col([
                html.Label("Show Recommended Only:", className="fw-bold"),
                dcc.Checklist(
                    id='bh-recommended-check',
                    options=[{'label': ' Recommended Items Only', 'value': 1}],
                    value=[],
                    inline=True
                )
            ], md=6),
        ], className="mb-4"),
        
        # CHARTS
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bh-age-vs-rating')
            ], md=6),
            
            dbc.Col([
                dcc.Graph(id='bh-feedback-dist')
            ], md=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bh-rec-by-age')
            ]),
        ]),
        
    ], fluid=True)
    
    return behavior_layout


def register_behavior_callbacks(app, df):
    """
    Register all callbacks for the Customer Behavior page.
    
    Args:
        app: Dash application
        df: Processed dataframe
    """
    @app.callback(
        [Output('bh-age-vs-rating', 'figure'),
         Output('bh-feedback-dist', 'figure'),
         Output('bh-rec-by-age', 'figure')],
        [Input('bh-class-dropdown', 'value'),
         Input('bh-recommended-check', 'value')]
    )
    def update_behavior_charts(selected_class, recommended_check):
        # Filter data
        filtered_df = df.copy()
        if selected_class != 'All':
            filtered_df = filtered_df[filtered_df['Class Name'] == selected_class]
        if recommended_check:
            filtered_df = filtered_df[filtered_df['Recommended IND'] == 1]
        
        # Chart 1: Age vs Rating
        fig1 = px.box(
            filtered_df,
            x='Rating',
            y='Age',
            title="Age Distribution by Rating",
            labels={'Age': 'Customer Age', 'Rating': 'Rating'},
            color_discrete_sequence=['#636EFA']
        )
        fig1.update_layout(height=400, template='plotly_white', showlegend=False)
        
        # Chart 2: Positive Feedback Distribution
        fig2 = px.histogram(
            filtered_df,
            x='Positive Feedback Count',
            nbins=30,
            title="Distribution of Positive Feedback Count",
            labels={'Positive Feedback Count': 'Feedback Count'},
            color_discrete_sequence=['#EF553B']
        )
        fig2.update_layout(height=400, template='plotly_white', showlegend=False)
        
        # Chart 3: Recommendation by Age Group
        rec_by_age = filtered_df.groupby('age_group')['Recommended IND'].agg(['mean', 'count']).reset_index()
        fig3 = px.bar(
            rec_by_age,
            x='age_group',
            y='mean',
            title="Recommendation Rate by Age Group",
            labels={'mean': 'Recommendation Rate', 'age_group': 'Age Group'},
            color_discrete_sequence=['#00CC96']
        )
        fig3.update_layout(height=400, template='plotly_white', showlegend=False)
        
        return fig1, fig2, fig3
