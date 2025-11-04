# ☁️ Qiu Huiting’s Weather App
# Uses the Open-Meteo API (no API key required)

import streamlit as st
import requests
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Qiu Huiting’s Weather App", page_icon="☁️", layout="centered")

# -------------------- CUSTOM STYLE --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #a3d8f4, #f7f7f7);
}
h1 {
    text-align: center;
    font-weight: 800;
    color: #1b3b5f;
}
p.subtitle {
    text-align: center;
    color: gray;
    margin-top: -10px;
    margin-bottom: 30px;
}
div[data-testid="stTextInput"] input {
    border-radius: 20px;
    background-color: white;
    padding: 10px 15px;
    font-size: 16px;
}
.stButton>button {
    background-color: #1b6ca8;
    color: white;
    border-radius: 20px;
    font-weight: 600;
    padding: 8px 25px;
}
.weather-card {
    background-color: white;
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("<h1>☁️ Qiu Huiting’s Weather App</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Check real-time temperature and humidity around the world</p>", unsafe_allow_html=True)

# -------------------- SEARCH BOX --------------------
city = st.text_input("Enter a city name:", value="Seoul")

# -------------------- API FUNCTIONS --------------------
def geocode_city(city_name):
    """Get latitude and longitude from Open-Meteo Geocoding API"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1}
    r = requests.get(url, params=params)
    data = r.json()
    results = data.get("results")
    if not results:
        return None
    item = results[0]
    return {
        "name": item["name"],
        "lat": item["latitude"],
        "lon": item["longitude"],
        "country": item.get("country", "")
    }

def get_weather(lat, lon):
    """Get weather data from Open-Meteo API"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code",
        "timezone": "auto"
    }
    r = requests.get(url, params=params)
    return r.json()

# -------------------- WEATHER ICONS --------------------
def weather_icon(code):
    icons = {
        0: "☀️ Clear sky",
        1: "🌤️ Mostly clear",
        2: "⛅ Partly cloudy",
        3: "☁️ Overcast",
        45: "🌫️ Fog",
        48: "🌫️ Fog",
        51: "🌦️ Light drizzle",
        61: "🌧️ Rain",
        71: "❄️ Snow",
        95: "⛈️ Thunderstorm"
    }
    return icons.get(code, "🌍 Weather data")

# -------------------- MAIN BUTTON --------------------
if st.button("🔍 Show Weather"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching weather data..."):
            info = geocode_city(city)
            if not info:
                st.error("City not found. Try another name.")
            else:
                weather = get_weather(info["lat"], info["lon"])
                current = weather.get("current", {})
                temp = current.get("temperature_2m")
                humidity = current.get("relative_humidity_2m")
                code = current.get("weather_code", 0)
                description = weather_icon(code)
                now = datetime.now().strftime("%Y-%m-%d %H:%M")

                st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
                st.markdown(f"### 📍 {info['name']}, {info['country']}")
                st.markdown(f"**Time:** {now}")
                st.markdown(f"**Temperature:** {temp}°C")
                st.markdown(f"**Humidity:** {humidity}%")
                st.markdown(f"**Condition:** {description}")
                st.markdown("</div>", unsafe_allow_html=True)
