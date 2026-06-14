import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Retail Intelligence Dashboard",
    layout="wide"
)

st.title("Retail Intelligence Dashboard")
st.write(
    "Analyze sales, identify top products, discover low-performing inventory, and generate business recommendations instantly."
)

uploaded_file = st.file_uploader(
    "Upload vendor sales CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    required_columns = [
        "Description",
        "Quantity",
        "UnitPrice",
        "InvoiceDate",
        "Country"
    ]

    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")

    else:
        df = df.drop_duplicates()
        df = df.dropna(subset=["Description"])

        df["InvoiceDate"] = pd.to_datetime(
            df["InvoiceDate"],
            errors="coerce"
        )

        df["Revenue"] = df["Quantity"] * df["UnitPrice"]

        st.sidebar.title("Retail Controls")
        st.sidebar.header("Filters")

        product_search = st.sidebar.text_input("Search Product")

        slow_product_limit = st.sidebar.number_input(
            "Show products sold less than or equal to",
            min_value=1,
            value=5
        )

        selected_country = st.sidebar.selectbox(
            "Select Country",
            ["All"] + sorted(df["Country"].dropna().unique().tolist())
        )

        if selected_country != "All":
            df = df[df["Country"] == selected_country]

        if product_search:
            df = df[
                df["Description"].str.contains(
                    product_search,
                    case=False,
                    na=False
                )
            ]

        returns = df[df["Quantity"] < 0]

        total_revenue = df["Revenue"].sum()

        total_returns = abs(
            (returns["Quantity"] * returns["UnitPrice"]).sum()
        )

        total_orders = (
            df["InvoiceNo"].nunique()
            if "InvoiceNo" in df.columns
            else len(df)
        )

        total_products = df["Description"].nunique()

        return_rate = (
            total_returns / total_revenue * 100
            if total_revenue != 0
            else 0
        )

        health_score = 100

        if return_rate > 10:
            health_score -= 20
        elif return_rate > 5:
            health_score -= 10

        if total_products < 20:
            health_score -= 10

        if total_revenue <= 0:
            health_score -= 30

        health_score = max(0, health_score)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Revenue", f"${total_revenue:,.2f}")

        with col2:
            st.metric("Total Returns", f"${total_returns:,.2f}")

        with col3:
            st.metric("Total Orders", total_orders)

        with col4:
            st.metric("Unique Products", total_products)

        with col5:
            st.metric("Business Health Score", f"{health_score}/100")

        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("Top 10 Products By Revenue")

            top_products = (
                df.groupby("Description")["Revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            st.bar_chart(top_products)

        with right:
            st.subheader("Slow Moving Products")

            slow_products = (
                df[df["Quantity"] > 0]
                .groupby("Description")
                .agg(
                    Units_Sold=("Quantity", "sum"),
                    Revenue=("Revenue", "sum")
                )
                .reset_index()
            )

            slow_products.columns = [
                "Product",
                "Units Sold",
                "Revenue"
            ]

            slow_products = slow_products[
                slow_products["Units Sold"] <= slow_product_limit
            ].sort_values(
                by="Units Sold",
                ascending=True
            )

            st.write(
                "These products sold the least. Consider giving discounts or bundle offers to clear stock."
            )

            st.dataframe(slow_products)

        best_product = (
            top_products.index[0]
            if len(top_products) > 0
            else "N/A"
        )

        least_product = (
            slow_products["Product"].iloc[0]
            if len(slow_products) > 0
            else "N/A"
        )

        st.subheader("Executive Summary")

        st.success(
            f"""
Business Health Score: {health_score}/100

Total revenue generated is ${total_revenue:,.2f}.

Return value is ${total_returns:,.2f}, with a return rate of {return_rate:.2f}%.

Best-performing product by revenue is {best_product}.

Slowest-moving product is {least_product}, which can be considered for discounts or bundle offers.
"""
        )

        st.divider()

        col6, col7 = st.columns(2)

        with col6:
            st.subheader("Discount Recommendation")

            discount_products = slow_products.copy()

            discount_products["Suggested Discount"] = discount_products[
                "Units Sold"
            ].apply(
                lambda x: "20%" if x <= 2 else "15%" if x <= 5 else "10%"
            )

            discount_products["Suggested Action"] = (
                "Offer discount or bundle with fast-selling products"
            )

            st.write(
                "These products are moving slowly. You can use discounts or bundle offers to clear them."
            )

            st.dataframe(discount_products)

            discount_csv = discount_products.to_csv(index=False)

            st.download_button(
                label="Download Discount Product List",
                data=discount_csv,
                file_name="discount_recommendations.csv",
                mime="text/csv"
            )

        with col7:
            st.subheader("Restock Recommendation")

            restock_products = (
                df[df["Quantity"] > 0]
                .groupby("Description")["Quantity"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            restock_products.columns = [
                "Product",
                "Units Sold"
            ]

            st.write(
                "These products are selling the most and should be considered for restocking."
            )

            st.dataframe(restock_products)

            restock_csv = restock_products.to_csv(index=False)

            st.download_button(
                label="Download Restock Product List",
                data=restock_csv,
                file_name="restock_recommendations.csv",
                mime="text/csv"
            )

        st.divider()

        st.subheader("Monthly Revenue Trend")

        df["Month"] = (
            df["InvoiceDate"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_revenue = (
            df.groupby("Month")["Revenue"]
            .sum()
        )

        st.line_chart(monthly_revenue)

        st.divider()

        st.subheader("Top 10 Countries By Revenue")

        country_revenue = (
            df.groupby("Country")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(country_revenue)

        st.divider()

        st.subheader("Download Filtered Data")

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_vendor_data.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload a CSV file to start analysis.")