from flask import Flask, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# ------------------------------
# GOOGLE SHEETS CONFIG
# ------------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1pt-Kn0JySRtAWxs-TZIakkM0q7VQ5bdZcIYhDp5r3uE" 
RANGE_NAME = "Sheet1!A:D"  # assuming columns: date | title | time | location

def get_events():
    """Fetch events directly from Google Sheets (no caching)."""
    creds = Credentials.from_service_account_file("/etc/secrets/service_account.json")
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    data = sheet.get_all_records()
    return data

@app.route("/")
def index():
    events = get_events()
    return render_template("index.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)

