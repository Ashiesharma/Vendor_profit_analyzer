import pandas as pd

df = pd.read_csv(
    "output/cleaned_online_retail.csv"
)

returns = df[
    df["Quantity"] < 0
]

print("\nTotal Return Records:")
print(len(returns))

returns["Return_Value"] = (
    returns["Quantity"]
    * returns["UnitPrice"]
)

print("\nTotal Return Value:")
print(returns["Return_Value"].sum())

top_returned = (
    returns.groupby("Description")["Quantity"]
    .sum()
    .sort_values()
    .head(10)
)

print("\nMost Returned Products:")
print(top_returned)
