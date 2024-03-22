"""
File: superstore_api.py
Description: API for accessing data from the superstore database

"""

import pandas as pd
import sqlite3

state_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    }

class SuperstoreAPI:
    con = None

    @staticmethod
    def connect(dbfile):
        """ make a connection to the database file"""
        SuperstoreAPI.con = sqlite3.connect(dbfile, check_same_thread=False)

    @staticmethod
    def execute(query):
        """ execute the query and return a dataframe"""
        return pd.read_sql_query(query, SuperstoreAPI.con)

    @staticmethod
    def get_category_list():
        """ get a list of categories"""
        query = 'SELECT DISTINCT Category FROM Superstore'
        df = SuperstoreAPI.execute(query)
        return list(df.Category)


    @staticmethod
    def get_profits_data(category):
        """ get total profit for each subcategory"""
        if category is None:
            return []
        else:
            query = (f"SELECT Sub_Category, SUM(Profit) AS TotalProfit FROM Superstore WHERE Category = '{category}' GROUP BY Sub_Category ORDER BY TotalProfit DESC")
            df = SuperstoreAPI.execute(query)
            return pd.DataFrame({'Sub_Category': df.Sub_Category,
                        'TotalProfit': df.TotalProfit})

    @staticmethod
    def get_year_list():
        """ get a list of years"""
        query = "SELECT DISTINCT strftime('%Y', Order_Date) AS Year FROM Superstore ORDER BY Year ASC"
        df = SuperstoreAPI.execute(query)
        return list(df.Year)

    @staticmethod
    def get_state_profit(year):
        """ get total profit per state for a given year"""
        if year is None:
            return []
        else:
            query = f"""
            SELECT States.State,
            IFNULL(SUM(ss.Profit), 0) AS TotalProfit
            FROM (SELECT DISTINCT State
                    FROM Superstore) AS States
            LEFT JOIN superstore ss ON States.State = ss.State AND strftime('%Y', ss.Order_Date) = '{year}'
            GROUP BY States.State;
            """
            df = SuperstoreAPI.execute(query)
            df['State_Abbrev'] = df['State'].map(state_abbrev)
            return pd.DataFrame({'State_Abbrev': df.State_Abbrev,
                                 'TotalProfit': df.TotalProfit})

    @staticmethod
    def get_monthly_profits(category):
        """ get profits for each category by month and year"""
        if category is None:
            return []
        else:
            query = f"""
            SELECT strftime('%m', Order_Date) AS Month, strftime('%Y', Order_Date) AS Year,
                            Category, SUM(Profit) AS TotalProfit
            FROM superstore
            WHERE Category = '{category}'
            GROUP BY strftime('%Y', Order_Date), strftime('%m', Order_Date);
            """
            df = SuperstoreAPI.execute(query)
            return pd.DataFrame({'Month': df.Month,
                                 'Year': df.Year,
                                 'TotalProfit': df.TotalProfit})