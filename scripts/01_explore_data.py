import pandas as pd 

Raw_Data_Path="Data/Online Retail.xlsx"

def load_raw_data(path=Raw_Data_Path):
    return pd.read_excel(path)

def profile_data(df):
     print("=== Shape ===")
     print(df.shape)

     print("\n=== Missing values ===")
     print(df.isnull().sum())

     print("\n=== Negative Quantity rows ===")
     print((df["Quantity"] < 0 ).sum())

     print("\n=== Non-positive UnitPrice rows ===")
     print((df["UnitPrice"] <= 0 ).sum())

     print("\n=== Top 5 countries by transaction count ===")
     print(df["Country"].value_counts().head(5))


if __name__ == "__main__":
     df= load_raw_data()
     profile_data(df)







