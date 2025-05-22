import pandas as pd
import streamlit as st

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        if "Timestamp" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def get_top_regions(df, metric="GHI", top_n=5):
    if "Region" not in df.columns:
        return pd.DataFrame({"Error": ["No 'Region' column found"]})
    return (
        df.groupby("Region")[metric]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
        .rename(columns={metric: f"Avg {metric}"})
    )