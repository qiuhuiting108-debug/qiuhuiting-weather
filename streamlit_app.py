# 🌍 Qiu Huiting’s Open-Meteo Interactive Weather Dashboard
# Interactive world map + city input + weather visualization using Open-Meteo API

import streamlit as st
import requests
import pandas as pd
from streamlit_folium import st_folium
import folium

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(page_title="Qiu Huiting’s Weather Dashboard", page_icon="🌍", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {background-color:#f7f7f7;}
h1 {text-align:center; font-weight:800; color:#1b3b5f;}
.sidebar .sidebar-content {background-color:#f4f6f9;}
.stButton > button {
    border-radius:20px;
    background-color:#1b6ca8;
    color:white;
    font-weight:600;
    padding:6px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>🌦️ Qiu Huiting’s Open-Meteo Interactive Weather Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Click on the world map or type a city name to visualize weather data.</p>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("🌍 Choose Location Method")
method = st.sidebar.radio("Select how to choose a location:", ["Click on Map", "Enter City Name"])

# ---------------- FUNCTIONS ----------------
def geocode_city(city):
    """Convert city name to coordinates"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1})
    data = r.json()
    results = data.get("results")
    if not results:
        return None
    item = results[0]
    return item["latitude"], item["longitude"], item["name"], item.get("country", "")

def get_weather(lat, lon, variable):
    """Get hourly weather data"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": variable,
        "forecast_days": 2,
        "timezone": "auto"
    }
    return requests.get(url, params=params).json()

# ---------------- MAIN LOGIC ----------------
if method == "Click on Map":
    st.markdown("## 🗺️ 1. Click anywhere on the map to select a location")

    # World map view
    m = folium.Map(location=[20, 0], zoom_start=2)
    map_data = st_folium(m, height=450, width=750)

    if map_data and map_data["last_clicked"]:
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        st.success(f"✅ Selected location: {lat:.2f}, {lon:.2f}")

        st.markdown("### 📊 2. Choose a variable to visualize:")
        variable = st.multiselect("Select weather variables:",
                                  ["temperature_2m", "relative_humidity_2m", "windspeed_10m"],
                                  default=["temperature_2m"])

        if st.button("Show Weather Data"):
            for var in variable:
                data = get_weather(lat, lon, var)
                hourly = data["hourly"]
                df = pd.DataFrame({
                    "time": hourly["time"],
                    var: hourly[var]
                })
                st.line_chart(df.set_index("time"))
            st.info("✅ Visualization complete!")

elif method == "Enter City Name":
    st.markdown("## 🏙️ 1. Type a city name")
    city = st.text_input("City name:", value="Seoul")

    st.markdown("### 📊 2. Choose a variable to visualize:")
    variable = st.multiselect("Select weather variables:",
                              ["temperature_2m", "relative_humidity_2m", "windspeed_10m"],
                              default=["temperature_2m"])

    if st.button("🔍 Show Data"):
        loc = geocode_city(city)
        if not loc:
            st.error("❌ City not found. Try another name.")
        else:
            lat, lon, name, country = loc
            st.success(f"📍 {name}, {country}  ({lat:.2f}, {lon:.2f})")

            for var in variable:
                data = get_weather(lat, lon, var)
                hourly = data["hourly"]
                df = pd.DataFrame({
                    "time": hourly["time"],
                    var: hourly[var]
                })
                st.line_chart(df.set_index("time"))
            st.info("✅ Visualization complete!")

