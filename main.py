import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_play_scraper import reviews


# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)  # A key file from Google API Console
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open('GooglePlay Reviews').sheet1

# Fetch reviews
package_name = 'com.ichi2.anki'
result, continuation_token = reviews(
    package_name,
    lang='en',
    count=10000,  # Number of reviews per request
    )

# Extract stars, text, and date for each review
reviews_data = [(review['score'], review['content'], str(review['at'])) for review in result]

# Batch write to Google Sheets (reducing the number of API write requests)
sheet.append_rows(reviews_data)

print(f"{len(reviews_data)} reviews saved to Google Sheets!")
