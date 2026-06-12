import pandas as pd

df = pd.read_csv(
    "output/cleaned_online_retail.csv"
)

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"]
)

df["Revenue"] = (
    df["Quantity"]
    * df["UnitPrice"]
)

df["Month"] = (
    df["InvoiceDate"]
    .dt.to_period("M")
)

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
)

print(monthly_sales)