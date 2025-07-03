
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Load dataset
df = pd.read_csv("sales_data.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Create Dash app
app = dash.Dash(__name__)
app.title = "Sales Analysis Dashboard"

# Layout
app.layout = html.Div([
    html.H1("📊 Sales Analysis Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Label("Select Product(s):"),
            dcc.Dropdown(
                id='product-filter',
                options=[{"label": p, "value": p} for p in df['Product'].unique()],
                value=[],
                multi=True,
                placeholder="Choose product(s)"
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            html.Label("Select Region(s):"),
            dcc.Dropdown(
                id='region-filter',
                options=[{"label": r, "value": r} for r in df['Region'].unique()],
                value=[],
                multi=True,
                placeholder="Choose region(s)"
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),

        html.Div([
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['Date'].min(),
                end_date=df['Date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '35%', 'display': 'inline-block'}),
    ], style={'margin': '20px'}),

    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart')
])

# Callback to update charts
@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('product-filter', 'value'),
     Input('region-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_dashboard(products, regions, start_date, end_date):
    dff = df.copy()
    if products:
        dff = dff[dff['Product'].isin(products)]
    if regions:
        dff = dff[dff['Region'].isin(regions)]
    if start_date and end_date:
        dff = dff[(dff['Date'] >= start_date) & (dff['Date'] <= end_date)]

    line_fig = px.line(dff, x='Date', y='Sales', color='Product', title='Sales Over Time')
    bar_fig = px.bar(dff, x='Region', y='Sales', color='Product', barmode='group', title='Sales by Region')

    return line_fig, bar_fig

# Run app
    if __name__ == '__main__':
        port=int(os.environ.get("PORT",8050))
        app.run(host="0.0.0.0",port=port,debug=True)
