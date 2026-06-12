import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("output/cleaned_online_retail.csv")

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")

plt.tight_layout()

os.makedirs("output", exist_ok=True)

plt.savefig("output/top_10_products.png")

plt.show()

print("Chart saved in output/top_10_products.png")