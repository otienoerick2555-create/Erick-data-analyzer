import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="SME Data Engine", page_icon="💼", layout="wide")

# --- CUSTOM CSS FOR A PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    h1 { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

st.title("💼 SME Data Engine")
st.write("Automated Data Cleaning & Sales Analytics for Kenyan Businesses.")

# --- TEMPLATE DOWNLOAD ---
def get_csv_template():
    template_data = "Date,Product,Category,Quantity_Sold,Revenue_KES,Location\n2024-05-01,Maize Flour,Grains,20,4000,Kisumu\n2024-05-01,Milk,Dairy,15,900,Kisumu\n2024-05-02,Cooking Oil,Grains,5,1500,Maseno\n2024-05-02,Milk,Dairy,10,600,Maseno"
    b64 = base64.b64encode(template_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sme_template.csv">📥 Download Blank Business Template</a>'
    return href
            # --- NEW: AUTOMATED INSIGHTS (The "Fake AI") ---
st.subheader("Automated Insights")    
        top_performer = grouped_data.iloc[0]
        bottom_performer = grouped_data.iloc[-1]
        
        st.success(f"📌 **Top Performer:** The highest total for **{target_metric}** is in **{top_performer[group_by]}** (Total: {top_performer[target_metric]:,.2f}). You should focus your resources here!")
        
        if len(grouped_data) > 1:st.warning(f"⚠️ **Lowest Performer:** The lowest total is in **{bottom_performer[group_by]}** (Total: {bottom_performer[target_metric]:,.2f}). You might need to investigate why this is lagging.")

st.markdown(get_csv_template(), unsafe_allow_html=True)
st.divider()

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload your Sales or Inventory Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Clean Column Names (Remove spaces, make lowercase)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Auto-Clean
        df = df.dropna(how='all')
        df = df.drop_duplicates()
        
        st.success(f"✅ Data processed successfully! Analyzed {len(df)} transactions.")
        
    except Exception as e:
        st.error("🚨 Oops! We couldn't read this file. Please ensure it's a valid Excel or CSV file.")
        st.stop()
else:
    st.info("👆 Please upload your business data. (Showing sample Duka data below).")
    df = pd.DataFrame({
        'date': ['2024-05-01', '2024-05-01', '2024-05-02', '2024-05-02', '2024-05-03'],
        'product': ['Maize Flour', 'Milk', 'Cooking Oil', 'Milk', 'Sugar'],
        'category': ['Grains', 'Dairy', 'Grains', 'Dairy', 'Groceries'],
        'quantity_sold': [20, 15, 5, 10, 30],
        'revenue_kes': [4000, 900, 1500, 600, 4500],
        'location': ['Kisumu', 'Kisumu', 'Maseno', 'Maseno', 'Kisumu']
    })

# --- ANALYTICS ENGINE ---
st.divider()

# Identify columns based on name (smart detection for Kenyan businesses)
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
text_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()

if len(numeric_cols) == 0:
    st.warning("⚠️ No number columns found. Please ensure your file has numbers like Quantity or Revenue.")
else:
    st.subheader("# The app looks at the column names to guess the context
cols = [c.lower() for c in df.columns]

if 'revenue' in cols or 'sales' in cols or 'price' in cols:
    st.subheader("💼 Business Performance Dashboard")
elif 'yield' in cols or 'crop' in cols or 'farm' in cols:
    st.subheader("🌾 Agricultural Yield Dashboard")
elif 'age' in cols or 'gender' in cols or 'respondent' in cols:
    st.subheader("🎓 Research Insights Dashboard")
else:
    st.subheader("📊 Data Insights Dashboard")")
    
    # Try to automatically guess the Revenue and Quantity columns
    rev_col = next((c for c in numeric_cols if 'rev' in c or 'amount' in c or 'total' in c), numeric_cols[0])
    qty_col = next((c for c in numeric_cols if 'qty' in c or 'quantity' in c), numeric_cols[0] if len(numeric_cols) > 1 else None)
    
    # Top Level Metrics
    total_rev = df[rev_col].sum()
    avg_rev = df[rev_col].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Total Revenue (KES)", f"{total_rev:,.2f}")
    col2.metric(f"Average Transaction (KES)", f"{avg_rev:,.2f}")
    if qty_col:
        col3.metric(f"Total Items Sold", f"{df[qty_col].sum():,.0f}")
    
    st.divider()

    # --- SMART CHARTS FOR BUSINESS ---
    st.subheader("📈 Sales Insights")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Top Products by Revenue
        if 'product' in df.columns:
            top_products = df.groupby('product')[rev_col].sum().reset_index().sort_values(by=rev_col, ascending=False).head(10)
            fig1 = px.bar(top_products, x='product', y=rev_col, title="Top 10 Best-Selling Products (By Revenue)", color='product')
            st.plotly_chart(fig1, use_container_width=True)
            
    with chart_col2:
        # Revenue by Location (if they have multiple shops)
        if 'location' in df.columns:
            loc_rev = df.groupby('location')[rev_col].sum().reset_index()
            fig2 = px.pie(loc_rev, names='location', values=rev_col, title="Revenue by Location/Shop", hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
        elif 'category' in df.columns:
             cat_rev = df.groupby('category')[rev_col].sum().reset_index()
             fig2 = px.pie(cat_rev, names='category', values=rev_col, title="Revenue by Category", hole=0.4)
             st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # --- DOWNLOAD CLEANED DATA ---
    st.subheader("📥 Download Your Cleaned Data")
    st.write("Use this clean file for your records or loan applications.")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name='clean_business_data.csv',
        mime='text/csv',
    )

    # --- CONTACT / HIRE ME BANNER ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("🚀 Need a Custom System?")
    st.sidebar.write("Want this app customized with your business logo and advanced features?")
    st.sidebar.markdown("**Contact Erick:**")
    st.sidebar.write("📞 0141 325 479")
            # --- NEW: AUTOMATED INSIGHTS (The "Fake AI") ---
        st.subheader("🤖 Automated Insights")
        top_performer = grouped_data.iloc[0]
        bottom_performer = grouped_data.iloc[-1]
        
        st.success(f"📌 **Top Performer:** The highest total for **{target_metric}** is in **{top_performer[group_by]}** (Total: {top_performer[target_metric]:,.2f}). You should focus your resources here!")
        
        if len(grouped_data) > 1:
            st.warning(f"⚠️ **Lowest Performer:** The lowest total is in **{bottom_performer[group_by]}** (Total: {bottom_performer[target_metric]:,.2f}). You might need to investigate why this is lagging.")
    st.sidebar.write("📧 otienoerick2555@gmail.com")

    with st.expander("View Raw Data"):
        st.dataframe(df, use_container_width=True)
