import pandas as pd
import os
from sqlalchemy import create_engine
import urllib
import logging
import time
from ingestion_db import ingest_db

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(engine):
    '''This function will merge the different tabel to get the overall vendor summary and adding new columns in the resultant data'''
    vendor_sales_summary = pd.read_sql_query("""WITH FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(TRY_CAST(Freight AS FLOAT)) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Volume,
            pp.Price AS ActualPrice,
            SUM(TRY_CAST(p.Quantity AS FLOAT)) AS TotalPurchaseQuantity,
            SUM(TRY_CAST(p.Dollars AS FLOAT)) AS TotalPurchaseDollars
        FROM purchases AS p
        JOIN purchase_prices AS pp
            ON p.Brand = pp.Brand
        WHERE TRY_CAST(p.PurchasePrice AS FLOAT) > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Volume, pp.Price
    ),

    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(TRY_CAST(SalesDollars AS FLOAT)) AS TotalSalesDollars,
            SUM(TRY_CAST(SalesPrice AS FLOAT)) AS TotalSalesPrice,
            SUM(TRY_CAST(SalesQuantity AS FLOAT)) AS TotalSalesQuantity,
            SUM(TRY_CAST(ExciseTax AS FLOAT)) AS TotalExciseTax
        FROM Sales
        GROUP BY VendorNo, Brand
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary AS ps
    LEFT JOIN SalesSummary AS ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary AS fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """,engine)
    return vendor_sales_summary
    
def clean_data(df):
    ''' This function will clean the data '''
    # changing datatypes to float/int
    df['Volume'] = df['Volume'].astype('float64')
    df['VendorNumber'] = df['VendorNumber'].astype('int64')
    df['Brand'] = df['Brand'].astype('int64')
    df['PurchasePrice'] = df['PurchasePrice'].astype('float64')
    df['ActualPrice'] = df['ActualPrice'].astype('float64')
    df['TotalPurchaseQuantity'] = df['TotalPurchaseQuantity'].astype('int64')    

    # removing spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    
    # Creating new columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit']/df['TotalSalesDollars'])*100
    df['StockTurnover'] = df['TotalSalesQuantity']/df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars']/df['TotalPurchaseDollars']

    # filling missing value, inf, -inf and NaN with 0
    df.replace([float('inf'), float('-inf')], 0, inplace=True)
    df.fillna(0,inplace = True)
    
    return df

if __name__=='__main__':
    # Creating database connection
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

    logging.info('Creating Vendor Summary Table.....')
    summary_df = create_vendor_summary(engine)
    logging.info(summary_df.head())

    logging.info('Cleaning Data....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting Data....')
    ingest_db(clean_df,'vendor_sales_summary',engine)
    logging.info('Completed')