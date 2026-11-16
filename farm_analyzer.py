import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Universal Data Analyzer", page_icon="📊", layout="wide")
st.title("📊 Erick's Universal Data Analyzer")
st.write("Upload any CSV file (Business, Agriculture, Research) to instantly generate insights.")

# --- TEMPLATE DOWNLOAD ---
def get_csv_template():
    template_data = "Category,Item,Quantity,Sales_Amount\nRegion A,Product X,10,5000\nRegion B,Product Y,5,2000"
    b64 = base64.b64encode(template_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="universal_template.csv">📥 Download Blank Data Template</a>'
    return href

st.markdown(get_csv_template(), unsafe_allow_html=True)
st.divider()

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload your data file (CSV format)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
else:
    st.info("👆 Please upload a CSV file. (Showing sample Business data below until you upload).")
    df = pd.DataFrame({
        'Region': ['Nairobi', 'Mombasa', 'Kisumu', 'Nairobi', 'Mombasa'],
        'Product': ['Laptop', 'Phone', 'Tablet', 'Phone', 'Laptop'],
        'Units_Sold': [5, 10, 3, 8, 4],
        'Revenue': [250000, 150000, 60000, 120000, 200000]
    })

# --- THE UNIVERSAL ANALYTICS ENGINE ---
st.divider()

# 1. Automatically detect Number columns and Text columns
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()

if len(numeric_cols) == 0:
    st.error("⚠️ Your file has no number columns to analyze. Please ensure your data has numbers (like Sales, Age, Quantity).")
else:
    st.subheader("⚙️ Customize Your Analysis")
    
    colA, colB = st.columns(2)
    
    with colA:
        # User picks the number they want to analyze (e.g., Revenue, Yield)
        target_metric = st.selectbox("What number do you want to analyze?", numeric_cols)
        
    with colB:
        # User picks how to group it (e.g., By Region, By Crop, By Name)
        if len(categorical_cols) > 0:
            group_by = st.selectbox("Group the results by:", ["None (Analyze Everything)"] + categorical_cols)
        else:
            group_by = "None (Analyze Everything)"

    # --- KEY METRICS ---
    st.subheader("Key Metrics")
    total_sum = df[target_metric].sum()
    total_avg = df[target_metric].mean()
    total_max = df[target_metric].max()
    
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Total {target_metric}", f"{total_sum:,.2f}")
    col2.metric(f"Average {target_metric}", f"{total_avg:,.2f}")
    col3.metric(f"Maximum {target_metric}", f"{total_max:,.2f}")

    # --- CHARTS ---
    st.subheader("Visual Insights")
    
    if group_by != "None (Analyze Everything)":
        # Group the data and create a bar chart
        grouped_data = df.groupby(group_by)[target_metric].sum().sort_values(ascending=False)
        st.bar_chart(grouped_data)
        st.write(f"*Showing Total {target_metric} by {group_by}*")
    else:
        st.info("Select a 'Group by' option above to see a bar chart.")

    st.divider()

    # --- RAW DATA ---
    with st.expander("View Your Raw Data"):
        st.dataframe(df, use_container_width=True)
