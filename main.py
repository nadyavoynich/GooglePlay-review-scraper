from google_play_scraper import Sort, reviews

# import gspread
# import pandas as pd
# from oauth2client.service_account import ServiceAccountCredentials


# Set up the credentials (! a JSON key file from Google API Console)
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
# client = gspread.authorize(credentials)

package_name = 'com.ichi2.anki'

all_reviews = []
continuation_token = None  # Start with no token

while True:
    result, continuation_token = reviews(
        package_name,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=100,  # Number of reviews per request
        continuation_token=continuation_token  # Token to fetch the next page of reviews
    )

    # Add the reviews from this batch to the list
    all_reviews.extend(result)

    # Break the loop if no more reviews are available
    if continuation_token is None:
        break

# Extract stars and text for each review
reviews_data = [(review['score'], review['content']) for review in all_reviews]

# Print the reviews
for stars, text in reviews_data:
    print(f"Stars: {stars}, Review: {text}")

# Create a new spreadsheet or open an existing one
# sheet = client.create("AnkiDroid")
# worksheet = sheet.get_worksheet(0)

# Save the data to Google Sheets
# df = pd.DataFrame(reviews_data, columns=['Stars', 'Review'])
# worksheet.update([df.columns.values.tolist()] + df.values.tolist())
