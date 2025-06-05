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

# Dropdown/combobox options (example lists, replace with actual values)
portfolio_options = ["portfolio_1", "portfolio_2", "portfolio_3"]
cluster_options = ["cluster_1", "cluster_2", "cluster_3"]

# Combobox allows typing or selecting existing options
portfolio_slug = st.combobox("Portfolio Slug", portfolio_options, help="Type to search or enter a new portfolio slug.")
cluster_slug = st.combobox("Cluster Slug", cluster_options, help="Type to search or enter a new cluster slug.")


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
