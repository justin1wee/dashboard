"""
File: xlsx_to_db.py
Description: converts the xslx file to sqlite database
"""

import pandas as pd
import sqlite3

# reads xls file into dataframe and removes quotation marks from columns
df_store = pd.read_excel('Superstore.xls')
df_store.columns = df_store.columns.str.replace('"', '')

# Define the name for database
db_name = 'Superstore.db'

# Create a connection. This also creates the .db file if it doesn't exist.
conn = sqlite3.connect(db_name)

# Write the DataFrame to the SQLite DB
# Replace 'table_name' with your preferred table name
df_store.to_sql('superstore', conn, if_exists='replace', index=False)

# Close the connection
conn.close()