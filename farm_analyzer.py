import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Farm Yield Analyzer", page_icon="🌾", layout="wide")
st.title("🌾 Agricultural Yield Analyzer")
st.write("Upload your farm data below to instantly generate charts and insights.")

# --- NEW: Create a Downloadable Template ---
def get_csv_template():
    template_data = "Farmer_Name,Crop,Acres_Planted,Yield_Kg\nJohn Doe,Maize,10,5000\nJane Doe,Beans,5,2000"
    b64 = base64.b64encode(template_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="farm_template.csv">📥 Download Blank Data Template</a>'
    return href

st.markdown(get_csv_template(), unsafe_allow_html=True)
st.divider()

# --- NEW: The File Uploader ---
uploaded_file = st.file_uploader("Upload your farm data (CSV format)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully! Here is your analysis:")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
else:
    st.info("👆 Please upload a CSV file. (Showing demo data below until you upload).")
    df = pd.DataFrame({
        'Farmer_Name': ['Otieno', 'Wanjiku', 'Otieno', 'Kamau', 'Wanjiku', 'Kamau'],
        'Crop': ['Maize', 'Beans', 'Beans', 'Maize', 'Maize', 'Beans'],
        'Acres_Planted': [5, 3, 2, 10, 4, 5],
        'Yield_Kg': [2500, 1200, 800, 6000, 2100, 1900]
    })

# --- THE ANALYTICS ENGINE ---
try:
    st.sidebar.header("Filter Data")
    selected_crop = st.sidebar.selectbox("Select a Crop:", ["All"] + list(df['Crop'].dropna().unique()))
    
    if selected_crop != "All":
        filtered_df = df[df['Crop'] == selected_crop]
    else:
        filtered_df = df

    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    total_acres = filtered_df['Acres_Planted'].sum()
    total_yield = filtered_df['Yield_Kg'].sum()
    avg_yield_per_acre = total_yield / total_acres if total_acres > 0 else 0
    
    col1.metric("Total Acres Planted", f"{total_acres:,.1f} Acres")
    col2.metric("Total Yield", f"{total_yield:,.0f} Kg")
    col3.metric("Avg Yield per Acre", f"{avg_yield_per_acre:,.1f} Kg/Acre")

    st.divider()

    st.subheader("Yield by Farmer")
    farmer_yield = filtered_df.groupby('Farmer_Name')['Yield_Kg'].sum().sort_values(ascending=False)
    st.bar_chart(farmer_yield)

    st.divider()

    st.subheader("Your Uploaded Data")
    st.dataframe(filtered_df, use_container_width=True)

except KeyError:
    st.error("⚠️ Error: The columns in your file do not match. Please make sure your CSV has the exact columns: 'Farmer_Name', 'Crop', 'Acres_Planted', 'Yield_Kg'.")
