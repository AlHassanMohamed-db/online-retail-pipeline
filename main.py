import importlib

explore = importlib.import_module("scripts.01_explore_data")
clean = importlib.import_module("scripts.02_clean_and_split")
load = importlib.import_module("scripts.03_load_to_sql")


def run_pipeline():

    df = explore.load_raw_data()
    explore.profile_data(df)

    clean_sales , unknown_customer_sales , suspicious_pricing = clean.split_data(df)
    clean.verify_split(df,clean_sales,unknown_customer_sales,suspicious_pricing)

    load.load_tables(clean_sales, unknown_customer_sales, suspicious_pricing)

if __name__=="__main__" :
    run_pipeline()


