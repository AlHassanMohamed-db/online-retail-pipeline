import importlib
import logging

logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(levelname)s - %(message)s',
     handlers= [
          logging.FileHandler('Pipeline.log'),
          logging.StreamHandler(),
     ],
)


explore = importlib.import_module("scripts.01_explore_data")
clean = importlib.import_module("scripts.02_clean_and_split")
load = importlib.import_module("scripts.03_load_to_sql")


def run_pipeline():
    logging.info('Pipeline Started')

    try:

     df = explore.load_raw_data()
     logging.info(f'Row data loaded : {df.shape[0]} rows , {df.shape[1]} colums') 

     explore.profile_data(df)

     clean_sales , unknown_customer_sales , suspicious_pricing = clean.split_data(df)
     clean.verify_split(df,clean_sales,unknown_customer_sales,suspicious_pricing)
     logging.info(f'Split Complete : clean = {len (clean_sales)},'
                  f' unknown_customer_sales= {len(unknown_customer_sales)},'
                  f'suspicious_pricing= {len(suspicious_pricing)}')

     load.load_tables(clean_sales, unknown_customer_sales, suspicious_pricing)
    except Exception as e :
       logging.error(f'Pipeline failed = {e}') 
       raise  

if __name__=="__main__" :
    run_pipeline()


