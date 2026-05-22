from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================
# LOAD & PREPARE DATA
# ============================================

df = pd.read_csv("data/Womens Clothing E-Commerce Reviews.csv")
df = df.drop(columns=["Unnamed: 0"], errors='ignore')
df = df.dropna(subset=["Division Name", "Department Name", "Class Name"])
df["Review Text"] = df["Review Text"].fillna("")
df["Title"] = df["Title"].fillna("")
df["review_length"] = df["Review Text"].str.len()
df["is_trend"] = (df["Department Name"] == "Trend").astype(int)
df["age_group"] = pd.cut(df["Age"], bins=[0, 25, 35, 45, 55, 100], labels=["<25", "25-35", "35-45", "45-55", "55+"])
df["log_feedback"] = np.log1p(df["Positive Feedback Count"])

# ============================================
# INITIALIZE APP
# ============================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# ============================================
# NAVBAR
# ============================================

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

# ============================================
# PAGE 1: OVERVIEW
# ============================================

page_overview = dbc.Container([
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

# ============================================
# PAGE 2: CUSTOMER BEHAVIOR
# ============================================

page_behavior = dbc.Container([
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

# ============================================
# PAGE 3: PRODUCT INSIGHTS
# ============================================

page_products = dbc.Container([
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

# ============================================
# PAGE 4: CORRELATIONS & TRENDS
# ============================================

page_trends = dbc.Container([
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

# ============================================
# MAIN LAYOUT
# ============================================

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
], fluid=True, style={"padding": "0px"})

# ============================================
# ROUTING CALLBACK
# ============================================

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/behavior':
        return page_behavior
    elif pathname == '/products':
        return page_products
    elif pathname == '/trends':
        return page_trends
    else:
        return page_overview

# ============================================
# PAGE 1 CALLBACKS
# ============================================

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

# ============================================
# PAGE 2 CALLBACKS
# ============================================

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

# ============================================
# PAGE 3 CALLBACKS
# ============================================

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

# ============================================
# PAGE 4 CALLBACKS
# ============================================

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

# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":
    app.run(debug=True, port=8050)