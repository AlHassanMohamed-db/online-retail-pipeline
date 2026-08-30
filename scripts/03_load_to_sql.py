import os
import pyodbc
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

DB_SERVER =os.getenv("DB_SERVER")
DB_DATABASE= os.getenv("DB_DATABASE")


def get_raw_connection():
    conn_str=(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        "Trusted_Connection=yes;"
        # NOTE: Encrypt=no disables TLS entirely. This is acceptable ONLY
        # because the SQL Server instance is local (same machine, no
        # network traffic leaves the host). In any remote/production
        # setup this must be replaced with a properly trusted certificate
        # and encryption left enabled (Encrypt=yes).
        "Encrypt=no;"
    ) 
    return pyodbc.connect(conn_str)


def get_engine():
    return create_engine("mssql+pyodbc://" , creator=get_raw_connection)


def load_tables(clean_sales, unknown_customer_sales, suspicious_pricing):
    engine= get_engine()

    tables = {
        "clean_sales" : clean_sales,
        "unknown_customer_sales" : unknown_customer_sales,
        "suspicious_pricing" : suspicious_pricing
    }
   
    for table_name , df in tables.items():
        logging.info(f"Uploading table '{table_name}' ({len(df)} rows)")
        df.to_sql(table_name,engine,if_exists = "replace" , index=False)
        logging.info(f"table '{table_name}' uploaded successfully")

    logging.info("All tables uploaded successfully!")

if __name__ == "__main__":
     print("Run this script's load_tables() with your cleaned DataFrames.")

  