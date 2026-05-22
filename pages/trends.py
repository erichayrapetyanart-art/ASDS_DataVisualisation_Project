"""
Correlations & Trends page module.
Analyzes relationships and trend vs non-trend product performance.
"""

from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def get_trends_layout(df):
    """
    Create the layout for the Correlations & Trends page.
    
    Args:
        df: Processed dataframe
    
    Returns:
        dbc.Container: Page layout
    """
    trends_layout = dbc.Container([
        html.Br(),
        
        html.H3("Correlations & Trend Analysis", className="fw-bold mb-4"),
        
        # CORRELATION MATRIX
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='tr-correlation-heatmap')
            ]),
        ], className="mb-4"),
        
        html.Hr(),
        
        # TRENDS SECTION
        html.H4("Trend vs Non-Trend Products", className="fw-bold mb-4 mt-4"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='tr-ratings-trend')
            ], md=6),
            
            dbc.Col([
                dcc.Graph(id='tr-review-length-trend')
            ], md=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='tr-feedback-dist-trend')
            ], md=6),
            
            dbc.Col([
                dcc.Graph(id='tr-log-feedback-trend')
            ], md=6),
        ]),
        
    ], fluid=True)
    
    return trends_layout


def register_trends_callbacks(app, df):
    """
    Register all callbacks for the Correlations & Trends page.
    
    Args:
        app: Dash application
        df: Processed dataframe
    """
    @app.callback(
        [Output('tr-correlation-heatmap', 'figure'),
         Output('tr-ratings-trend', 'figure'),
         Output('tr-review-length-trend', 'figure'),
         Output('tr-feedback-dist-trend', 'figure'),
         Output('tr-log-feedback-trend', 'figure')],
        Input('url', 'pathname')
    )
    def update_trends_charts(pathname):
        try:
            # Prepare data - remove NaN values for cleaner visualization
            df_clean = df.dropna(subset=["Rating", "Age", "Positive Feedback Count", "review_length"])
            
            # Chart 1: Correlation Matrix
            cols = ["Rating", "Recommended IND", "Positive Feedback Count", "review_length", "Age"]
            corr_matrix = df_clean[cols].corr()
            
            fig1 = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                zmin=-1,
                zmax=1,
                text=np.round(corr_matrix.values, 2),
                texttemplate='%{text}',
                textfont={"size": 11},
                colorbar=dict(title="Correlation")
            ))
            fig1.update_layout(
                title="Correlation Matrix of Key Behavioral Features",
                height=500,
                template='plotly_white',
                xaxis={'side': 'bottom'}
            )
            
            # Chart 2: Ratings - Trend vs Non-Trend
            fig2 = px.box(
                df_clean,
                x='is_trend',
                y='Rating',
                title="Ratings: Trend vs Non-Trend Products",
                labels={'is_trend': 'Product Type', 'Rating': 'Rating'},
                color_discrete_sequence=['#636EFA'],
                category_orders={'is_trend': [0, 1]}
            )
            fig2.update_xaxes(ticktext=['Non-Trend', 'Trend'], tickvals=[0, 1])
            fig2.update_layout(height=400, template='plotly_white', showlegend=False)
            
            # Chart 3: Review Length - Trend vs Non-Trend
            fig3 = px.box(
                df_clean,
                x='is_trend',
                y='review_length',
                title="Review Length: Trend vs Non-Trend Products",
                labels={'is_trend': 'Product Type', 'review_length': 'Review Length'},
                color_discrete_sequence=['#EF553B'],
                category_orders={'is_trend': [0, 1]}
            )
            fig3.update_xaxes(ticktext=['Non-Trend', 'Trend'], tickvals=[0, 1])
            fig3.update_layout(height=400, template='plotly_white', showlegend=False)
            
            # Chart 4: Positive Feedback Distribution - Trend vs Non-Trend
            fig4 = px.histogram(
                df_clean,
                x='Positive Feedback Count',
                nbins=25,
                color='is_trend',
                title="Positive Feedback Distribution: Trend vs Non-Trend",
                labels={'Positive Feedback Count': 'Feedback Count', 'is_trend': 'Product Type'},
                barmode='overlay',
                color_discrete_map={0: '#00CC96', 1: '#AB63FA'}
            )
            fig4.update_xaxes(title_text='Positive Feedback Count')
            fig4.update_layout(height=400, template='plotly_white')
            
            # Chart 5: Log Feedback - Trend vs Non-Trend
            df_clean_log = df_clean[df_clean['log_feedback'].notna()]
            fig5 = px.box(
                df_clean_log,
                x='is_trend',
                y='log_feedback',
                title="Log(Positive Feedback Count): Trend vs Non-Trend Products",
                labels={'is_trend': 'Product Type', 'log_feedback': 'Log Feedback Count'},
                color_discrete_sequence=['#FFA15A'],
                category_orders={'is_trend': [0, 1]}
            )
            fig5.update_xaxes(ticktext=['Non-Trend', 'Trend'], tickvals=[0, 1])
            fig5.update_layout(height=400, template='plotly_white', showlegend=False)
            
            return fig1, fig2, fig3, fig4, fig5
        
        except Exception as e:
            print(f"Error in trends callback: {e}")
            import traceback
            traceback.print_exc()
            # Return empty figures if error occurs
            empty_fig = go.Figure()
            empty_fig.add_annotation(text=f"Error: {str(e)}", showarrow=False)
            return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
