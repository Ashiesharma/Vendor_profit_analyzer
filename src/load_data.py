import pandas as pd

df = pd.read_csv("data/online_retail.csv")

print("First 5 Rows:")
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nShape:")
print(df.shape)