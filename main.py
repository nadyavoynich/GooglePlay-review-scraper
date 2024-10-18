import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_play_scraper import reviews


# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)  # A key file from Google API Console
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open('GooglePlay Reviews').sheet1

package_name = 'com.ichi2.anki'

# Fetch reviews
result, continuation_token = reviews(
    package_name,
    lang='en',
    count=1000,  # Number of reviews per request
    )

# Extract stars, text, and date for each review and save to Google Sheets
if result:
    for review in result:
        stars, text, date = review['score'], review['content'], review['at']

        # Append a row to the sheet with stars, review text, and date
        sheet.append_row([stars, text, str(date)])

    print(f"{len(result)} reviews saved to Google Sheets!")
else:
    print("No reviews found")
