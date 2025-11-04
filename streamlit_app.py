# 🌦️ Qiu Huiting’s Open-Meteo Interactive Weather Dashboard
# English version — with world map, variable selector, and city search option

import streamlit as st
import requests
import pandas as pd
from streamlit_folium import st_folium
import folium

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(page_title="Qiu Huiting’s Weather Dashboard", page_icon="🌦️", layout="wide")

# ---------------- CUSTOM STYLE ----------------
st.markdown("""
<style>
body {background-color: #f7f7f7;}
h1 {text-align:center; font-weight:800; color:#1b3b5f;}
p.subtitle {text-align:center; color:gray; margin-top:-10px; margin-bottom:30px;}
.sidebar .sidebar-content {background-color:#f4f6f9;}
.stButton>button {
    border-radius: 20px;
    background-color: #1b6ca8;
    color: white;
    font-weight: 600;
    padding: 8px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>🌍 Open-Meteo Interactive Weather Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Click on the world map or enter a city name to visualize live weather data.</p>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("🌎 Location Selection")
method = st.sidebar.radio("Select location method:", ["Click on Map", "Enter City Name"])

# ---------------- FUNCTIONS ----------------
def geocode_city(city):
    """Convert city name to coordinates."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1})
    data = r.json()
    results = data.get("results")
    if not results:
        return None
    item = results[0]
    return item["latitude"], item["longitude"], item["name"], item.get("country", "")

def get_weather(lat, lon, variables):
    """Fetch weather data from Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(variables),
        "forecast_days": 2,
        "timezone": "auto"
    }
    return requests.get(url, params=params).json()

# ---------------- MAIN LAYOUT ----------------
if method == "Click on Map":
    st.markdown("## 1️⃣ Click on the map to select a location")

    m = folium.Map(location=[20, 0], zoom_start=2)
    map_data = st_folium(m, height=450, width=750)

    if map_data and map_data["last_clicked"]:
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        st.success(f"✅ Selected coordinates: {lat:.2f}, {lon:.2f}")

        st.markdown("### 📊 2️⃣ Choose variables to visualize:")
        variables = st.multiselect(
            "Select weather variables:",
            {
                "temperature_2m": "Temperature (°C)",
                "precipitation": "Precipitation (mm)",
                "windspeed_10m": "Wind Speed (m/s)",
                "relative_humidity_2m": "Relative Humidity (%)"
            },
            default=["temperature_2m"]
        )

        if st.button("Show Weather Data"):
            weather = get_weather(lat, lon, variables)
            hourly = weather.get("hourly", {})
            times = hourly.get("time", [])
            df = pd.DataFrame({"time": times})
            for var in variables:
                df[var] = hourly.get(var, [None] * len(times))
            df["time"] = pd.to_datetime(df["time"])
            df = df.set_index("time")
            st.line_chart(df)
            st.info("✅ Weather data visualized successfully!")

elif method == "Enter City Name":
    st.markdown("## 1️⃣ Type a city name")
    city = st.text_input("Enter city name:", value="Seoul")

    st.markdown("### 📊 2️⃣ Choose variables to visualize:")
    variables = st.multiselect(
        "Select weather variables:",
        {
            "temperature_2m": "Temperature (°C)",
            "precipitation": "Precipitation (mm)",
            "windspeed_10m": "Wind Speed (m/s)",
            "relative_humidity_2m": "Relative Humidity (%)"
        },
        default=["temperature_2m"]
    )

    if st.button("🔍 Show Weather Data"):
        loc = geocode_city(city)
        if not loc:
            st.error("❌ City not found. Please try another name.")
        else:
            lat, lon, name, country = loc
            st.success(f"📍 {name}, {country}  ({lat:.2f}, {lon:.2f})")

            weather = get_weather(lat, lon, variables)
            hourly = weather.get("hourly", {})
            times = hourly.get("time", [])
            df = pd.DataFrame({"time": times})
            for var in variables:
                df[var] = hourly.get(var, [None] * len(times))
            df["time"] = pd.to_datetime(df["time"])
            df = df.set_index("time")
            st.line_chart(df)
            st.info("✅ Weather data visualized successfully!")
