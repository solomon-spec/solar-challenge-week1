### app/main.py
import streamlit as st
import plotly.express as px

from utils import load_data, get_top_regions



st.title("☀️ Solar Data Dashboard")

# Country and data source mapping
country_map = {
    "Benin": "https://drive.google.com/uc?export=download&id=1agfPwNJAOc5nzWVnXt49-djmDshvdiI_",
    "Sierra Leone": "https://drive.google.com/uc?export=download&id=17YZErwPwjhEUUdfV6kPZRHFoSxMZHZ2-",
    "Togo": "https://drive.google.com/uc?export=download&id=1BpWrG_eKsAAnhmKMebA8iiM5xe79yyjY"
}

# User selections
selected_country = st.selectbox("Choose a country", list(country_map.keys()))
metric = st.radio("Select a metric", ["GHI", "DNI", "DHI"])

# Load and display data
df = load_data(country_map[selected_country])

if df is not None:
    st.write("### Sample Data")
    st.write(df.head())

    st.subheader(f"{metric} Over Time in {selected_country}")
    if df["Timestamp"].notna().any() and df[metric].notna().any():
        fig = px.line(df, x="Timestamp", y=metric, title=f"{metric} Over Time")
        st.plotly_chart(fig)
    else:
        st.warning(f"No valid data for {metric} over time.")

    st.subheader(f"Boxplot of {metric}")
    if df[metric].notna().any():
        box_fig = px.box(df, y=metric, title=f"Distribution of {metric}")
        st.plotly_chart(box_fig)
    else:
        st.warning(f"No valid data for {metric} boxplot.")

    st.subheader("Top Regions by Average GHI")
    top_df = get_top_regions(df, metric="GHI", top_n=5)
    st.dataframe(top_df)
else:
    st.warning("Data could not be loaded. Please check the file URL.")