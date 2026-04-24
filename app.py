import streamlit as st
import pandas as pd


st.title("🏢 Business Directory Search")
# Load and filter
df = pd.read_csv('leads_cleaned.csv')
districts = df['District'].fillna("Unknown").astype(str).unique().tolist()
category = st.selectbox("Select Category", ["All"] + sorted(df['Category'].unique().tolist()))
district = st.selectbox("Select District", ["All"] + sorted(districts))

if category != "All":
    df = df[df['Category'] == category]
if district != "All":
    df = df[df['District'] == district]


st.write(f"Found {len(df)} businesses")
st.dataframe(df)