from google_play_scraper import reviews, Sort
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# Set up the credentials (! a JSON key file from Google API Console)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
client = gspread.authorize(credentials)

package_name = 'com.ichi2.anki'

all_reviews = []
page_num = 1
while True:
    result, _ = reviews(
        package_name,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=100,  # Number of reviews per request
        continuation_token=None  # For paginating to the next set of reviews
    )

    if not result:
        break  # Stop if no more reviews

    all_reviews.extend(result)
    page_num += 1

reviews_data = [(review['score'], review['content']) for review in all_reviews]

for stars, text in reviews_data:
    print(f"Stars: {stars}, Review: {text}")

# Create a new spreadsheet or open an existing one
sheet = client.create("AnkiDroid")
worksheet = sheet.get_worksheet(0)

# Save the data to Google Sheets
df = pd.DataFrame(reviews_data, columns=['Stars', 'Review'])
worksheet.update([df.columns.values.tolist()] + df.values.tolist())
