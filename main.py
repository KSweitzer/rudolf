import praw
import os
from dotenv import load_dotenv
import pandas as pd

import elevenlabs

def create_ai_voice_file(audio, file_name):
    elevenlabs.save(audio, file_name)
    pass


def main():
    load_dotenv()
    reddit = praw.Reddit(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET"), user_agent=os.environ.get("USER_AGENT"))
    subreddit = reddit.subreddit("AmItheAsshole").hot()

    post_list = []

    for post in subreddit:
        post_list.append([post.title, post.score, post.url, post.num_comments, post.selftext])

    post_df = pd.DataFrame(post_list, columns=['title', 'score', 'url', 'num_comments', 'body'])

    # Now we need to create ai voice with this
    test = f"{post_df['body'][2].split(".")[0]}.{post_df['body'][2].split(".")[1]}.{post_df['body'][2].split(".")[2]}."

    audio = elevenlabs.generate(
        text=test,
        voice="Ethan",
        api_key=os.environ['ELEVEN_LABS_KEY']
    )

    elevenlabs.save(audio, "audio.mp3")

    pass


if __name__ == "__main__":
    main()
