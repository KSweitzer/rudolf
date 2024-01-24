import praw  # reddit
import os  # environment variables
from dotenv import load_dotenv  # environment variables
import pandas as pd  # pandas Dataframe
import elevenlabs  # AI voice
from pydub import AudioSegment  # combining mp3

def separate_post_body(post_body: str) -> list:
    ret = []
    seperated_post = post_body.split('.')

    curr_portion = ""
    for sentence in seperated_post:
        temp = f"{sentence}. "

        if len(curr_portion + temp) > 2500:
            ret.append(curr_portion[:len(curr_portion) - 1])
            curr_portion = f"{temp}"
        else:
            curr_portion += temp

    if len(ret) == 0:
        ret.append(curr_portion[:len(curr_portion) - 1])

    return ret


def main():
    # connect to reddit and get the hot posts
    load_dotenv()
    reddit = praw.Reddit(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET"),
                         user_agent=os.environ.get("USER_AGENT"))
    subreddit = reddit.subreddit("AmItheAsshole").hot()

    # save posts to data structures
    post_list = []  # for holding all info about the posts
    post_dict = {}  # for holding the data we need to make the tik toks

    # initializes the list and dict
    for i, post in enumerate(subreddit):
        if i == 0:
            continue
        post_list.append([post.title, post.score, post.url, post.num_comments, post.selftext])
        post_dict[post.title] = separate_post_body(post.selftext)

    # initializes the DataFrame
    # basically the same as the list but makes it easier if we want to record the analytics of the posts
    post_df = pd.DataFrame(post_list, columns=['title', 'score', 'url', 'num_comments', 'body'])

    #for post in post_dict:
    #    if len(post_dict[post]) == 1:
    #        audio = elevenlabs.generate(
    #            text=post_dict[post][0],
    #            voice="Adam",
    #            api_key=os.environ['ELEVEN_LABS_KEY']
    #        )
    #
    #        elevenlabs.save(audio, f"audio/{post}.mp3")

    #sound1 = AudioSegment.from_mp3("test.mp3")
    #sound2 = AudioSegment.from_mp3("audio.mp3")

    #combined = sound1 + sound2
    #combined.export("combined.mp3", format="mp3")
    # Now we need to create ai voice with this

    #audio = elevenlabs.generate(
    #    text=ret[0],
    #    voice="Adam",
    #    api_key=os.environ['ELEVEN_LABS_KEY']
    #)

    #elevenlabs.save(audio, "test.mp3")

    pass


if __name__ == "__main__":
    main()
