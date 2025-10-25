import pandas as pd
import os
from sqlalchemy import create_engine
import urllib
import logging
import time

# --- Logging Configuration ---
logging.basicConfig(
    filename="logs/ingestion_db_sqlserver.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

server = 'DESKTOP-JEM8O95\SQLEXPRESS'
database = 'InventoryDB'

# Windows Authentication connection string
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

params = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


def ingest_db(df, table_name, engine):
    """Ingest the dataframe into SQL Server database table"""
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    logging.info(f"Successfully ingested {table_name} into SQL Server")

def load_raw_data():
    """Load CSVs as dataframe and ingest into SQL Server DB"""
    start = time.time()

    for file in os.listdir('data'):
        if file.endswith('.csv'):
            try:
                df = pd.read_csv(os.path.join('data', file))
                logging.info(f"Ingesting {file} into SQL Server...")

                table_name = file[:-4]
                ingest_db(df, table_name, engine)

            except Exception as e:
                logging.error(f"Error while ingesting {file}: {e}")

    end = time.time()
    total_time = (end - start) / 60
    logging.info('-------------------Ingestion Complete-------------------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')

if __name__ == '__main__':
    load_raw_data()