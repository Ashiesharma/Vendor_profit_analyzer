import pandas as pd

df = pd.read_csv(
    "output/cleaned_online_retail.csv"
)

df["Revenue"] = (
    df["Quantity"]
    * df["UnitPrice"]
)

print("\nTotal Revenue:")
print(df["Revenue"].sum())

print("\nTop 10 Products By Revenue:")

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)