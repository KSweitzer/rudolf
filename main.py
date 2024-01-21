import praw
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    reddit = praw.Reddit(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET"), user_agent=os.environ.get("USER_AGENT"))
    subreddit = reddit.subreddit("AmItheAsshole").hot(limit=10)

    for submission in subreddit:
        print(submission.title)
    pass


if __name__ == "__main__":
    main()
