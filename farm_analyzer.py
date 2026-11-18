import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Erick Data Analyzer", page_icon="📊", layout="wide")

# --- SIDEBAR: YOUR BUSINESS INFO ---
st.sidebar.markdown("### 🚀 Need a Custom System?")
st.sidebar.write("Want this app customized with your business logo and advanced features?")
st.sidebar.markdown("**Contact Erick:**")
st.sidebar.write("📞 0141 325 479")
st.sidebar.write("📧 otienoerick2555@gmail.com")

st.title("📊 Erick Data Analyzer")
st.write("Professional Data Analysis. Upload Excel or CSV files to generate interactive insights.")

# --- TEMPLATE DOWNLOAD ---
def get_csv_template():
    template_data = "Date,Product,Category,Quantity_Sold,Revenue_KES,Location\n2024-05-01,Maize Flour,Grains,20,4000,Kisumu\n2024-05-01,Milk,Dairy,15,900,Kisumu\n2024-05-02,Cooking Oil,Grains,5,1500,Maseno"
    b64 = base64.b64encode(template_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data_template.csv">📥 Download Blank Data Template</a>'
    return href

st.markdown(get_csv_template(), unsafe_allow_html=True)
st.divider()

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Clean Column Names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Auto-Clean Data
        original_rows = len(df)
        df = df.dropna(how='all')
        df = df.drop_duplicates()
        
        st.success(f"✅ Data processed successfully! Cleaned {original_rows - len(df)} bad rows.")
        
    except Exception as e:
        st.error("🚨 Oops! We couldn't read this file. Please ensure it's a valid Excel or CSV file.")
        st.stop()
else:
    st.info("👆 Please upload your data. (Showing sample Business data below).")
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
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
text_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()

if len(numeric_cols) == 0:
    st.warning("⚠️ No number columns found. Please ensure your file has numbers like Quantity or Revenue.")
else:
    st.subheader("📊 Data Insights Dashboard")
    
    rev_col = next((c for c in numeric_cols if 'rev' in c or 'amount' in c or 'total' in c), numeric_cols[0])
    qty_col = next((c for c in numeric_cols if 'qty' in c or 'quantity' in c), numeric_cols[0] if len(numeric_cols) > 1 else None)
    
    total_rev = df[rev_col].sum()
    avg_rev = df[rev_col].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Total {rev_col.title()} (KES)", f"{total_rev:,.2f}")
    col2.metric(f"Average {rev_col.title()} (KES)", f"{avg_rev:,.2f}")
    if qty_col:
        col3.metric(f"Total {qty_col.title()}", f"{df[qty_col].sum():,.0f}")
    
    st.divider()

    st.subheader("📈 Interactive Visual Insights")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if 'product' in df.columns:
            top_products = df.groupby('product')[rev_col].sum().reset_index().sort_values(by=rev_col, ascending=False).head(10)
            fig1 = px.bar(top_products, x='product', y=rev_col, title=f"Top Products by {rev_col.title()}", color='product')
            st.plotly_chart(fig1, use_container_width=True)
            
    with chart_col2:
        if 'location' in df.columns:
            loc_rev = df.groupby('location')[rev_col].sum().reset_index()
            fig2 = px.pie(loc_rev, names='location', values=rev_col, title=f"{rev_col.title()} by Location", hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
        elif 'category' in df.columns:
             cat_rev = df.groupby('category')[rev_col].sum().reset_index()
             fig2 = px.pie(cat_rev, names='category', values=rev_col, title=f"{rev_col.title()} by Category", hole=0.4)
             st.plotly_chart(fig2, use_container_width=True)

    # --- AUTOMATED INSIGHTS ---
    st.subheader("🤖 Automated Insights")
    if 'location' in df.columns:
        grouped_data = df.groupby('location')[rev_col].sum().reset_index().sort_values(ascending=False, by=rev_col)
        top_performer = grouped_data.iloc[0]
        st.success(f"📌 **Top Performer:** The highest total for **{rev_col.title()}** is in **{top_performer['location']}** (Total: {top_performer[rev_col]:,.2f}). You should focus your resources here!")
    elif 'product' in df.columns:
        grouped_data = df.groupby('product')[rev_col].sum().reset_index().sort_values(ascending=False, by=rev_col)
        top_performer = grouped_data.iloc[0]
        st.success(f"📌 **Top Performer:** The best-selling product for **{rev_col.title()}** is **{top_performer['product']}** (Total: {top_performer[rev_col]:,.2f}). Make sure you never run out of stock!")

    st.divider()

    st.subheader("📥 Download Your Cleaned Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name='clean_data.csv',
        mime='text/csv',
    )

    with st.expander("View Raw Data"):
        st.dataframe(df, use_container_width=True)
