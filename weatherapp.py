# weatherapp.py
import streamlit as st
import requests
import datetime
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Auto-refresh every 60 seconds (60000 ms)
st_autorefresh(interval=60000, key="refresh")

# ------------------ Page style ------------------
page_bg = """
<style>
/* basic page + fonts */
body {
    background: linear-gradient(120deg, #f6d5f7 0%, #fbe9d7 100%);
    font-family: "Segoe UI", Roboto, Arial, sans-serif;
    margin: 0;
    padding: 0;
}

/* small fade-in for the whole page */
* { animation: fadeIn 0.6s ease-in-out; }
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* input styling */
input {
    background: rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    padding: 10px 12px !important;
    border: 2px solid #ff9dc9 !important;
    font-size: 16px !important;
    color: #ffb7d5 !important;
}
input::placeholder { color: #ffb7d5 !important; opacity: 0.8 !important; }
.stTextInput > div > div > input { color: #ffb7d5 !important; }

/* ---------- HOVER DEBUG BUBBLE ---------- */
#debug-hover {
    position: fixed;
    bottom: 20px;
    left: 20px;
    width: 48px;
    height: 48px;
    background: linear-gradient(180deg, #ffdff0, #ffd1e8);
    border-radius: 50%;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.14);
    cursor: default;
    z-index: 9999;
    font-size: 23px;
    color:#b23a6d;
    font-weight:800;
}

/* hidden bubble */
#debug-hover .bubble {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    left: 60px;
    bottom: 0px;
    width: 210px;
    padding: 12px;
    border-radius: 12px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    color:#ffb7d5;
    font-size: 13px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    transform: translateY(6px);
    transition: opacity 0.25s ease, transform 0.25s ease;
    white-space: normal;
    line-height: 1.35;
}

/* show bubble on hover */
#debug-hover:hover .bubble {
    visibility: visible;
    opacity: 1;
    transform: translateY(0px);
}

/* title */
.bubble-title {
    font-weight: 700;
    color: #ffe0f0;
    font-size: 14px;
    margin-bottom: 6px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ Config ------------------
API_KEY = os.getenv("OPEN_WEATHER_KEY")  

# Header
st.markdown("<h1 style='text-align:center; color:#ff6fb5; font-size:48px; margin-bottom:6px;'>🌸 Weather App 🌸</h1>",
            unsafe_allow_html=True)

# Input
city = st.text_input("Enter a city name :")

# ------------------ HOVER DEBUG BUBBLE GENERATOR ------------------
def render_hover_debug(lat, lon, month, hemisphere, season, offset):
    return f"""
    <div id="debug-hover">
        🌸
        <div class="bubble">
            <div class="bubble-title">Debug Info</div>
            <b>Latitude:</b> {lat}<br>
            <b>Longitude:</b> {lon}<br>
            <b>Month:</b> {month}<br>
            <b>Hemisphere:</b> {hemisphere}<br>
            <b>Season:</b> {season}<br>
            <b>TZ Offset:</b> {offset}s
        </div>
    </div>
    """

# ------------------ Main Logic ------------------
if city:
    request_city = requests.utils.requote_uri(city.strip())
    url = f"https://api.openweathermap.org/data/2.5/weather?q={request_city}&appid={API_KEY}&units=metric"

    try:
        resp = requests.get(url, timeout=8)
        data = resp.json()
    except Exception:
        st.error("Network error while contacting weather service.")
        st.stop()

    cod = data.get("cod")
    try: cod_int = int(cod)
    except: cod_int = None

    if cod_int != 200:
        st.error(data.get("message", "City not found."))
        st.stop()

    coord = data.get("coord") or {}
    lat = coord.get("lat", 0.0)
    lon = coord.get("lon", 0.0)

    timezone_offset = int(data.get("timezone", 0))
    utc_now = datetime.datetime.utcnow()
    city_time = utc_now + datetime.timedelta(seconds=timezone_offset)
    formatted_time = city_time.strftime("%I:%M:%S %p")
    month = city_time.month

    is_north = float(lat) >= 0
    hemisphere_text = "Northern Hemisphere" if is_north else "Southern Hemisphere"

    if is_north:
        season = "spring" if month in (3,4,5) else "summer" if month in (6,7,8) else "autumn" if month in (9,10,11) else "winter"
    else:
        season = "autumn" if month in (3,4,5) else "winter" if month in (6,7,8) else "spring" if month in (9,10,11) else "summer"

    # ------------------ Inject animations ------------------
    if season == "spring":
        st.markdown("""
        <style>
        @keyframes sakura-fall { 0%{transform:translateY(-18px) rotate(0);} 100%{transform:translateY(100vh) rotate(200deg);} }
        .sakura { position:fixed; top:-10px; font-size:16px; color:#ffb6d5; animation:sakura-fall 6s ease-in infinite; z-index:9998; pointer-events:none; }
        </style>
        <div class="sakura" style="left:10%;">❀</div>
        <div class="sakura" style="left:28%; animation-delay:1s;">❀</div>
        <div class="sakura" style="left:46%; animation-delay:2s;">❀</div>
        <div class="sakura" style="left:64%; animation-delay:0.6s;">❀</div>
        <div class="sakura" style="left:82%; animation-delay:1.8s;">❀</div>
        """, unsafe_allow_html=True)

    if season == "summer":
        st.markdown("""
        <style>
        @keyframes sparkle { 0%{opacity:0} 50%{opacity:1} 100%{opacity:0} }
        .spark { position:fixed; font-size:20px; color:#fff1a8; z-index:9998; animation:sparkle 2.2s infinite; pointer-events:none; }
        </style>
        <div class="spark" style="left:20%; top:18%;">✦</div>
        <div class="spark" style="left:65%; top:12%; animation-delay:1s;">✦</div>
        """, unsafe_allow_html=True)

    if season == "autumn":
        st.markdown("""
        <style>
        @keyframes leaf-fall { 0%{transform:translateY(-10px) rotate(0);} 100%{transform:translateY(100vh) rotate(180deg);} }
        .leaf { position:fixed; top:-10px; font-size:18px; color:#d77a32; animation:leaf-fall 6.5s linear infinite; z-index:9998; pointer-events:none; }
        </style>
        <div class="leaf" style="left:22%;">🍂</div>
        <div class="leaf" style="left:48%; animation-delay:1s;">🍂</div>
        <div class="leaf" style="left:74%; animation-delay:2s;">🍂</div>
        """, unsafe_allow_html=True)

    if season == "winter":
        st.markdown("""
        <style>
        @keyframes snow { 0%{transform:translateY(-10px)} 100%{transform:translateY(100vh)} }
        .snow { position:fixed; top:-10px; font-size:18px; color:white; animation:snow 7s linear infinite; z-index:9998; pointer-events:none; }
        </style>
        <div class="snow" style="left:12%;">❆</div>
        <div class="snow" style="left:34%; animation-delay:1.2s;">❆</div>
        <div class="snow" style="left:56%; animation-delay:2.1s;">❆</div>
        <div class="snow" style="left:78%; animation-delay:0.7s;">❆</div>
        """, unsafe_allow_html=True)

    # Inject rain if rainy
    weather_list = data.get("weather") or [{}]
    weather_main = str(weather_list[0].get("main", "")).lower()

    if "rain" in weather_main or "drizzle" in weather_main:
        st.markdown("""
        <style>
        @keyframes drop {
            0%{transform:translateY(-10px);opacity:1;}
            100%{transform:translateY(100vh);opacity:0;}
        }
        .drop { position:fixed; top:-10px; font-size:10px; color:rgba(173,216,230,0.9); animation:drop 1.2s linear infinite; z-index:9998; pointer-events:none; }
        </style>
        <div class="drop" style="left:14%;">●</div>
        <div class="drop" style="left:34%; animation-delay:0.2s;">●</div>
        <div class="drop" style="left:50%; animation-delay:0.5s;">●</div>
        <div class="drop" style="left:68%; animation-delay:0.7s;">●</div>
        <div class="drop" style="left:86%; animation-delay:1s;">●</div>
        """, unsafe_allow_html=True)

    # Inject hover bubble
    hover_html = render_hover_debug(lat, lon, month, hemisphere_text, season, timezone_offset)
    st.markdown(hover_html, unsafe_allow_html=True)

    # ------------------ Weather display ------------------
    main = data.get("main") or {}
    wind = data.get("wind") or {}

    temp = main.get("temp", "N/A")
    description = str(weather_list[0].get("description", "N/A")).capitalize()
    humidity = main.get("humidity", "N/A")
    wind_speed = wind.get("speed", "N/A")
    icon_code = weather_list[0].get("icon")

    # Time Box
    st.markdown(
        f"""
        <div style="
            text-align:center;
            margin-top:12px;
            background: rgba(55,55,65,0.55);
            padding:10px 18px;
            border-radius:12px;
            font-size:18px;
            color:#ffb7d5;
            width:fit-content;
            margin-left:auto;
            margin-right:auto;
            box-shadow:0 6px 14px rgba(0,0,0,0.1);
        ">
            🕒 Local Time in {city.title()}: {formatted_time}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Weather card
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.92);
            padding:22px;
            border-radius:16px;
            width:340px;
            margin:20px auto 30px auto;
            box-shadow:0 12px 30px rgba(0,0,0,0.12);
            backdrop-filter: blur(8px);
            text-align:center;
        ">
            <h2 style="color:#ff6fb5; font-size:40px; margin:6px 0;">{temp}°C</h2>
            <h4 style="color:#555; margin:6px 0; font-size:18px;">{description}</h4>
            <p style="color:#666; margin:6px 0;">💧 Humidity: {humidity}%</p>
            <p style="color:#666; margin:6px 0;">🌬 Wind: {wind_speed} m/s</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if icon_code:
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        st.image(icon_url, width=110)

else:
    st.info("Type a city name above to see the weather.")
