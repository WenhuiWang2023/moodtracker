import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import plotly.express as px
import json, os

# --- Connect to Google Sheets ---
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("ModeTracker").sheet1
    return sheet

sheet = connect_sheet()

# --- UI ---
st.set_page_config(page_title="Mood Logger", page_icon="🧠")
st.title("🧠 Mood Logger")

mood_options = {
    "😊": "Happy",
    "😐": "Neutral",
    "😔": "Sad",
    "😠": "Angry",
    "😴": "Tired",
    "😫": "Overwhelmed"
}

emoji = st.selectbox("Pick your mood:", options=list(mood_options.keys()))
note = st.text_input("Optional note (e.g., 'lots of Rx delays today')")

if st.button("Submit Mood"):
    timestamp = datetime.now().isoformat()
    sheet.append_row([timestamp, emoji, note])
    st.success(f"Logged: {emoji} - {mood_options[emoji]}")

st.markdown("---")
st.subheader("📊 Today's Mood Summary")

# --- Load and process data ---
def load_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    return df

df = load_data()

# --- Filter today's data ---
if not df.empty:
    df_today = df[df["timestamp"].dt.date == datetime.today().date()]
    mood_counts = df_today["mood"].value_counts().reset_index()
    mood_counts.columns = ["mood", "count"]
    
    if not mood_counts.empty:
        fig = px.bar(mood_counts, x="mood", y="count", title="Mood Count for Today")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No moods logged today yet.")
else:
    st.info("No mood data found.")
