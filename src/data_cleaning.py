import pandas as pd

df=pd.read_csv("data/online_retail.csv")
print("Orignal shape")
print(df.shape)
df=df.drop_duplicates()
df=df.dropna(subset=["Description"])
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
print("\nCleaned shape")
print(df.shape)
print("\nMissing Values:")
print(df.isnull().sum())
df.to_csv(
    "output/cleaned_online_retail.csv",
    index=False
)

print("\nCleaned dataset saved!")