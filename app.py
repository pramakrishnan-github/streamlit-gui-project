import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime
from requests.auth import HTTPBasicAuth

st.title("Posted Actuals Visualized")

# Input fields for authentication
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Dropdown options (example lists, replace these with actual values)
portfolio_options = ["example_portfolio_country"]
cluster_options = ["example_country_wind", "example_country_solar"]

# Dropdown selection widgets
portfolio_slug = st.selectbox("Portfolio Slug", portfolio_options)
cluster_slug = st.selectbox("Cluster Slug", cluster_options)

# Date selection widget
date_selected = st.date_input("Select Created Date", datetime.today())

# API request function
def fetch_data(url, auth):
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Proceed only if username and password are provided
if username and password:
    auth = HTTPBasicAuth(username, password)
    BASE_URL = f"https://api.dexterenergyservices.com/v1/portfolio/{portfolio_slug}/cluster/{cluster_slug}/actuals/latest/"
    data = fetch_data(BASE_URL, auth)

    if data:
        results = data.get("results", [])

        # Filter by the selected date
        filtered_results = [r for r in results if pd.to_datetime(r['created']).date() == date_selected]

        if filtered_results:
            asset_data = filtered_results[0]

            df = pd.DataFrame({
                "Interval Start": pd.to_datetime(asset_data["interval_start"]),
                "Load": asset_data["load"]
            })

            chart = alt.Chart(df).mark_line().encode(
                x='Interval Start:T',
                y='Load:Q'
            ).properties(
                title=f"Load Data for {asset_data['asset']} on {date_selected}"
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available for selected date.")
