import praw
import os
from dotenv import load_dotenv
import pandas as pd


def main():
    load_dotenv()
    reddit = praw.Reddit(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET"), user_agent=os.environ.get("USER_AGENT"))
    subreddit = reddit.subreddit("AmItheAsshole").hot()

    post_list = []

    for post in subreddit:
        post_list.append([post.title, post.score, post.url, post.num_comments, post.selftext])

    post_df = pd.DataFrame(post_list, columns=['title', 'score', 'url', 'num_comments', 'body'])
    print(post_df.head())

    # Now we need to create ai voice with this
    pass


if __name__ == "__main__":
    main()
