import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Vendor Profit Analyzer",
    layout="wide"
)

st.title("Vendor Profit Analyzer")

df = pd.read_csv(
    "output/cleaned_online_retail.csv"
)

df["Revenue"] = df["Quantity"] * df["UnitPrice"]
st.sidebar.header("Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].unique().tolist())
)

if selected_country != "All":
    df = df[df["Country"] == selected_country]

returns = df[df["Quantity"] < 0]

total_revenue = df["Revenue"].sum()

total_returns = abs(
    (returns["Quantity"] * returns["UnitPrice"]).sum()
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "Total Returns",
        f"${total_returns:,.2f}"
    )

st.subheader("Top 10 Products By Revenue")

top_products = (
    df.groupby("Description")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

st.bar_chart(top_products)
st.subheader("Monthly Revenue Trend")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
)

st.line_chart(monthly_revenue)
st.subheader("Top 10 Countries By Revenue")

country_revenue = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(country_revenue)
st.subheader("Download Filtered Data")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_vendor_data.csv",
    mime="text/csv"
)