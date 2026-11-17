import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SME Data Engine",
    page_icon="💼",
    layout="wide"
)

# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.main {
    background-color: #f9f9f9;
}
h1 {
    color: #1f77b4;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER
# ==========================================

st.title("💼 SME Data Engine")

st.write(
    "Automated Data Cleaning & Sales Analytics "
    "for Kenyan Businesses."
)

# ==========================================
# 4. CSV TEMPLATE DOWNLOAD
# ==========================================

def get_csv_template():

    template_data = (
        "Date,Product,Category,Quantity_Sold,"
        "Revenue_KES,Location\n"
        "2024-05-01,Maize Flour,Grains,20,4000,Kisumu\n"
        "2024-05-01,Milk,Dairy,15,900,Kisumu\n"
        "2024-05-02,Cooking Oil,Grains,5,1500,Maseno\n"
        "2024-05-02,Milk,Dairy,10,600,Maseno"
    )

    b64 = base64.b64encode(
        template_data.encode()
    ).decode()

    href = (
        f'<a href="data:file/csv;base64,{b64}" '
        'download="sme_template.csv">'
        '📥 Download Business Data Template</a>'
    )

    return href


st.markdown(
    get_csv_template(),
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# 5. FILE UPLOADER
# ==========================================

uploaded_file = st.file_uploader(
    "Upload your Sales or Inventory Data",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

    except Exception as e:

        st.error(f"Unable to read your file: {e}")
        st.stop()

else:

    st.info(
        "Showing sample Kenyan Duka business data. "
        "Upload your own file to analyse your business."
    )

    df = pd.DataFrame({

        "date": [
            "2024-05-01",
            "2024-05-01",
            "2024-05-02",
            "2024-05-02",
            "2024-05-03"
        ],

        "product": [
            "Maize Flour",
            "Milk",
            "Cooking Oil",
            "Milk",
            "Sugar"
        ],

        "category": [
            "Grains",
            "Dairy",
            "Grains",
            "Dairy",
            "Groceries"
        ],

        "quantity_sold": [20, 15, 5, 10, 30],

        "revenue_kes": [
            4000, 900, 1500, 600, 4500
        ],

        "location": [
            "Kisumu",
            "Kisumu",
            "Maseno",
            "Maseno",
            "Kisumu"
        ]

    })

# ==========================================
# 6. DATA CLEANING ENGINE
# ==========================================

st.divider()

# Standardize column names

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove empty rows and duplicate records

initial_rows = len(df)

df = df.dropna(how="all")
df = df.drop_duplicates()

removed_rows = initial_rows - len(df)

st.subheader("🧹 Data Cleaning Report")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))

col2.metric("Duplicates/Empty Rows Removed", removed_rows)

col3.metric("Total Columns", len(df.columns))

# ==========================================
# 7. AUTOMATIC DASHBOARD DETECTION
# ==========================================

cols = df.columns.tolist()

if any("revenue" in c or "sales" in c for c in cols):

    st.subheader("💼 Business Performance Dashboard")

elif any("yield" in c or "crop" in c or "farm" in c for c in cols):

    st.subheader("🌾 Agricultural Data Dashboard")

elif any("age" in c or "gender" in c or "respondent" in c for c in cols):

    st.subheader("🎓 Research Insights Dashboard")

else:

    st.subheader("📊 Data Insights Dashboard")

# ==========================================
# 8. NUMERIC COLUMN DETECTION
# ==========================================

numeric_cols = df.select_dtypes(
    include=["number"]
).columns.tolist()

text_cols = df.select_dtypes(
    include=["object", "string"]
).columns.tolist()

if not numeric_cols:

    st.warning(
        "No numerical columns found. "
        "Please upload data containing numerical values."
    )

else:

    # ======================================
    # 9. REVENUE AND QUANTITY DETECTION
    # ======================================

    rev_col = next(
        (
            c for c in numeric_cols
            if any(word in c for word in
                   ["revenue", "sales", "amount", "total"])
        ),
        None
    )

    qty_col = next(
        (
            c for c in numeric_cols
            if "quantity" in c or "qty" in c
        ),
        None
    )

    # ======================================
    # 10. KEY BUSINESS METRICS
    # ======================================

    st.subheader("📊 Key Performance Indicators")

    if rev_col:

        total_rev = df[rev_col].sum()

        avg_rev = df[rev_col].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Revenue (KES)",
            f"{total_rev:,.2f}"
        )

        col2.metric(
            "Average Transaction (KES)",
            f"{avg_rev:,.2f}"
        )

        if qty_col:

            col3.metric(
                "Total Items Sold",
                f"{df[qty_col].sum():,.0f}"
            )

        # ==================================
        # 11. SALES CHARTS
        # ==================================

        st.divider()

        st.subheader("📈 Sales Insights")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            if "product" in df.columns:

                top_products = (
                    df.groupby("product")[rev_col]
                    .sum()
                    .reset_index()
                    .sort_values(
                        by=rev_col,
                        ascending=False
                    )
                    .head(10)
                )

                fig1 = px.bar(
                    top_products,
                    x="product",
                    y=rev_col,
                    title="Top 10 Products by Revenue",
                    color="product"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

        with chart_col2:

            if "location" in df.columns:

                loc_rev = (
                    df.groupby("location")[rev_col]
                    .sum()
                    .reset_index()
                )

                fig2 = px.pie(
                    loc_rev,
                    names="location",
                    values=rev_col,
                    title="Revenue by Location",
                    hole=0.4
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            elif "category" in df.columns:

                cat_rev = (
                    df.groupby("category")[rev_col]
                    .sum()
                    .reset_index()
                )

                fig2 = px.pie(
                    cat_rev,
                    names="category",
                    values=rev_col,
                    title="Revenue by Category",
                    hole=0.4
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

        # ==================================
        # 12. AUTOMATED BUSINESS INSIGHTS
        # ==================================

        st.divider()

        st.subheader("🤖 Automated Business Insights")

        group_by = None

        for candidate in ["product", "category", "location"]:

            if candidate in df.columns:

                group_by = candidate
                break

        if group_by:

            grouped_data = (
                df.groupby(group_by)[rev_col]
                .sum()
                .reset_index()
                .sort_values(
                    by=rev_col,
                    ascending=False
                )
            )

            if not grouped_data.empty:

                top_performer = grouped_data.iloc[0]

                st.success(
                    f"🏆 Top Performer: "
                    f"{top_performer[group_by]} generated "
                    f"KES {top_performer[rev_col]:,.2f}."
                )

                if len(grouped_data) > 1:

                    bottom_performer = grouped_data.iloc[-1]

                    st.warning(
                        f"⚠️ Lowest Performer: "
                        f"{bottom_performer[group_by]} generated "
                        f"KES {bottom_performer[rev_col]:,.2f}. "
                        f"Investigate possible reasons for this performance."
                    )

    else:

        st.info(
            "No revenue column detected. "
            "You can still explore your numerical data below."
        )

    # ======================================
    # 13. DOWNLOAD CLEANED DATA
    # ======================================

    st.divider()

    st.subheader("📥 Download Your Cleaned Data")

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="clean_business_data.csv",
        mime="text/csv"
    )

# ==========================================
# 14. RAW DATA VIEW
# ==========================================

with st.expander("View Raw and Cleaned Data"):

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================================
# 15. CONTACT INFORMATION
# ==========================================

st.sidebar.markdown("---")

st.sidebar.subheader("🚀 Need a Custom System?")

st.sidebar.write(
    "Want this application customized "
    "with your business logo and advanced features?"
)

st.sidebar.markdown("**Contact Erick:**")

st.sidebar.write("📞 0141 325 479")

st.sidebar.write("📧 otienoerick2555@gmail.com")

st.sidebar.markdown("---")

st.sidebar.caption(
    "SME Data Engine | Built with Python & Streamlit"
)
