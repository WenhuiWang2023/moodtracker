# 🧠 Mood Logger App

A quick internal tool to track and visualize moods using Streamlit + Google Sheets.

## Features
- Log moods with emojis + notes
- Automatically stored in Google Sheets
- Daily summary bar chart (Plotly)

## Setup

1. Clone this repo
2. Set up Google Sheets and Google Cloud service account
3. For local version app_local.app, rename your credentials file to `credentials_moodtracker.json` and place in project root 
4. Run the app streamlit run app_local.py
5. For steamlit cloud version, paste the content of credential file in Secret of app as GOOGLE_CREDS = "<your_entire_JSON_string_here>". The json string can be generate using following python code:
import json

with open("credentials_moodtracker.json") as f:
    creds = f.read()

print(json.dumps(creds))
