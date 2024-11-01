import pandas as pd

filename = "Customer_Behaviour.xlsx"

def import_data(filename:str): #check for CSV!! does read_excel read csv??  could if statement it? 
    df = pd.read_excel(filename)
    return df

def filter_data(df:pd.DataFrame):
    filter1 = df["CustomerID"].isna()
    filter2 = df["Quantity"] < 0
    filter3 = df["UnitPrice"] < 0
    df_filtered = df[~filter1, ~filter2, ~filter3]
    return df_filtered

def loyalty_customers(df:pd.DataFrame, min_purchases:int) -> pd.DataFrame: #check it looks right 
    purchase_count = df.groupby("CustomerID").size()
    df_loyal = purchase_count[purchase_count >= min_purchases]
    df_loyal = df_loyal.reset_index(name="PurchaseCount")
    return df_loyal

def quarterly_revenue(df:pd.DataFrame):
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%d/%m/%Y") #convert to datetime
    df["Quarter"] = df["InvoiceDate"].dt.to_period("Q") #add a quarter column
    quarterly_revenue = df.groupby("Quarter")["UnitPrice"].sum() #group by quarter and total revenue 
    return quarterly_revenue

def high_demand_products(df:pd.DataFrame, top_n:int):
    totals = df.groupby("Description")["Quantity"].sum() #groups by item description and sums quantity of each item
    sorted_products = totals.sort_values(by="Quantity", ascending=False) #sort values by quantity in descending order, resulting in toppest highest
    top_products = sorted_products.head(top_n) #returns the toppest values based on inputted argument. 
    return top_products 


def purchase_patterns(df: pd.DataFrame) -> pd.DataFrame:    
    return df.groupby("Description").agg(avg_quantity = ("Quantity", "mean"), avg_unit_price=("UnitPrice", "mean")) #aggregates based on mean quantity/mean unit price of product


data = import_data(filename)

filtered_data = filter_data(data)

loyal_customers = loyalty_customers(filtered_data, 5)

revenue_summary = quarterly_revenue(filtered_data)

top_products = high_demand_products(filtered_data, 5)

buying_patterns = purchase_patterns(filtered_data)

print(filtered_data.head())
