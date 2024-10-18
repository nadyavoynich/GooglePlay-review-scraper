import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_play_scraper import Sort, reviews


# Google Sheets setup (a JSON key file from Google API Console)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet (replace 'your_google_sheet_name' with the actual name)
sheet = client.open('GooglePlay Reviews').sheet1  # Opens the first sheet

package_name = 'com.ichi2.anki'

# Fetch reviews
result, continuation_token = reviews(
    package_name,
    lang='en',
    # country='us',
    # sort=Sort.NEWEST,
    count=1,  # Number of reviews per request
    # continuation_token=continuation_token  # Token to fetch the next page of reviews
    )

# Extract stars, text, and date for the reviews
if result:
    stars, text, date = result[0]['score'], result[0]['content'], result[0]['at']

    # Save the review data into Google Sheets
    # Append a row to the sheet with stars, review text, and date
    sheet.append_row([stars, text, str(date)])

    print("Review saved to Google Sheets!")
else:
    print("No reviews found")
