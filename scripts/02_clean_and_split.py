import pandas as pd

Raw_Data_Path= "data/Online Retail.xlsx"

def load_raw_data(Path=Raw_Data_Path):
    return pd.read_excel(Path)

def split_data(df):

    suspicious_pricing = df[df["UnitPrice"] <= 0]
    remaining = df[df["UnitPrice"] > 0]

    unknown_customer_sales = remaining[remaining["CustomerID"].isnull()]
    clean_sales  =  remaining[remaining["CustomerID"].notnull()]

    return clean_sales , unknown_customer_sales , suspicious_pricing

def  verify_split(df,clean_sales,unknown_customer_sales,suspicious_pricing):
    total_split=len(clean_sales) + len(suspicious_pricing)+len(unknown_customer_sales)

    original_total = len(df)

    print(f"Original rows: {original_total}")
    print(f"Split total:   {total_split}")

    if total_split == original_total :
        print("Reconciliation check passed: no rows lost or duplicated.")

    else :
        print("WARNING: row counts do not match! Review the split logic.")



if __name__ == "__main" :
    df = load_raw_data()
    clean_sales,unknown_customer_sales,suspicious_pricing=split_data(df)
    verify_split(df,clean_sales,unknown_customer_sales,suspicious_pricing)

