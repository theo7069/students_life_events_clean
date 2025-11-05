from flask import Flask, render_template
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)

# --------------------------------------------
# GOOGLE SHEETS CONFIG
# --------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1pt-Kn0JySRtAWxs-TZIakkM0q7VQ5bdZcIYhDp5r3uE"
SERVICE_ACCOUNT_PATH = "/etc/secrets/service_account.json"

def get_events():
    """Fetch events directly from Google Sheets (no caching)."""
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        data = sheet.get_all_records()
        return data
    except Exception as e:
        # Print error in Render logs for debugging
        print("Error fetching data from Google Sheets:", e)
        # Return empty list instead of crashing
        return []

@app.route("/")
def index():
    events = get_events()
    return render_template("index.html", events=events)

# Flask entry point for local testing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
