"""
File: dashboard.py
Author: Justin Wee, Andy Lin
Description: .py file to create the dashboard for Superstore Data
"""

import pandas as pd
from superstore_api import SuperstoreAPI
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


def main():

    # initialize API
    api = SuperstoreAPI()
    api.connect('Superstore.db')

    # create the dash app
    app = Dash(__name__)

    # create the layout for the dashboard
    app.layout = html.Div([

        # title
        html.H2('Superstores: An Interactive Dashboard of Superstore Profits'),

        # Left column - bar chart
        html.Div([
        html.P('Select Category: '),
        dcc.Dropdown(id='category', options=api.get_category_list(), value='Furniture', style={'width': '100%'}),
        dcc.Graph(id='graph', style={'width': '100%', 'display': 'inline-block'}),
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Right column - heatmap
        html.Div([
        html.P('Select Year: '),
        dcc.Dropdown(id='year', options=api.get_year_list(), value=2014, style={'width': '100%'}),
        dcc.Graph(id='densitygraph', figure={}, style={'width': '100%', 'display': 'inline-block'}),
        ], style={'width': '45%', 'display': 'inline-block', 'marginLeft': '10%', 'verticalAlign': 'top'}),

        # Bottom - line graph
        html.Div([
        html.P('Click Category (or multiple): '),
        dcc.Checklist(id='checklist', options=api.get_category_list(), value=['Furniture'], inline=True),
        dcc.Graph(id='linegraph')
        ])
        ])

    # create a bar chart of profits by category with an interactive dropdown of categories
    @app.callback(
        Output('graph', 'figure'),  # Update the figure of the graph
        Input('category', 'value')
    )

    def update_graph(selected_category):
        # Get data of profits by category
        profits_data = api.get_profits_data(category=selected_category)

        # Calculate if positive or negative profit for color purposes
        profits_data['Profit_Sign'] = ['Positive' if x > 0 else 'Negative' for x in
                                             profits_data['TotalProfit']]

        # Create bar chart
        fig = px.bar(profits_data, x='Sub_Category', y='TotalProfit',
                     color='Profit_Sign',
                     color_discrete_map={'Positive': 'green', 'Negative': 'red'},
                     title=f'Profits by Sub-Category for the {selected_category} Category'
                     )

        return fig


    # create a heatmap of profits by state with an interactive dropdown of years
    @app.callback(
        Output('densitygraph', 'figure'),
        Input('year', 'value')
    )

    def choropleth_graph(year):

        # get state profit data by year
        state_data = api.get_state_profit(year=year)

        # create choropleth graph to illustrate profit by state
        fig = px.choropleth(
            data_frame=state_data,
            locationmode='USA-states',
            locations='State_Abbrev',
            scope='usa',
            color='TotalProfit',
            title=f'Total Profit across United States in {year}'
        )
        return fig

    # creates a line graph to map profits by category over time
    @app.callback(
        Output('linegraph', 'figure'),
        [Input('checklist', 'value')]
    )
    # create function to make line graph of all category profits by month and year
    def get_category_graph(category_list):
        # initialize dataframe to hold all data
        all_data = pd.DataFrame()

        # iterates through each category in list and finds profits by month, year
        for category in category_list:
            category_data = api.get_monthly_profits(category)
            category_data['Category'] = category
            # concatenates it to all_data dataframe
            all_data = pd.concat([all_data, category_data])

        # makes sure data is sorted by year and month to plot chronologically
        all_data['Year'] = all_data['Year'].astype(int)  # Ensure Year is an integer
        all_data['Month'] = all_data['Month'].astype(int)  # Ensure Month is an integer
        all_data.sort_values(by=['Year', 'Month'], inplace=True)

        # plot
        fig = px.line(data_frame=all_data,
                      x=pd.to_datetime(all_data[['Year', 'Month']].assign(DAY=1)),  # Convert Year and Month to datetime
                      y="TotalProfit",
                      color="Category",  # This will create a separate line for each category
                      title="Monthly Profits by Category",
                      labels={"TotalProfit": "Total Profit"},
                      markers=True)  # Adds markers to each data point

        # update layout
        fig.update_layout(xaxis_title="Year-Month",
                          yaxis_title="Profit",
                          legend_title="Category",
                          xaxis=dict(tickformat="%Y-%m"))  # Format x-axis labels as Year-Month

        return fig


    # run it
    app.run_server(debug=True)

main()



