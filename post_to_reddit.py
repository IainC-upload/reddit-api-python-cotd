import os
import json
import gspread
import praw
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet_data():
    # Load credentials from the environment variable
    creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    
    client = gspread.authorize(creds)
    sheet = client.open("Reddit Card of the Day").sheet1  # Ensure this matches your sheet name
    data = sheet.row_values(1)  # Get the first row
    
    if len(data) < 2:
        raise ValueError("Sheet must have at least two columns: title and text")
    
    return data[0], data[1]

def post_to_reddit(title, text):
    # Authenticate with Reddit
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent="google-sheets-bot"
    )
    
    subreddit = os.getenv("REDDIT_SUBREDDIT")
    reddit.subreddit(subreddit).submit(title, selftext=text)

def main():
    try:
        print("Fetching Google Sheet data...")
        title, text = get_google_sheet_data()
        print(f"Title: {title}")
        print(f"Text: {text[:50]}...")  # Print a snippet for privacy

        print("Posting to Reddit...")
        post_to_reddit(title, text)
        print("Post successful!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
