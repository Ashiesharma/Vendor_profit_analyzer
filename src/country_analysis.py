import pandas as pd

df = pd.read_csv(
    "output/cleaned_online_retail.csv"
)

df["Revenue"] = (
    df["Quantity"]
    * df["UnitPrice"]
)

top_countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop Countries By Revenue:\n")

print(top_countries)