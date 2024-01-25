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

    # saving body audio
    for post in post_dict:
        # creates audio directories if they do not exist
        if not os.path.isdir("temp"):
            os.mkdir("temp")
        if not os.path.isdir("audio"):
            os.mkdir("audio")

        # list of the separated segments of the body text
        body_lst = post_dict[post]

        # creates first audio segment
        ai_audio_seg = elevenlabs.generate(
            text=body_lst[0],
            voice="Adam",
            api_key=os.environ['ELEVEN_LABS_KEY']
        )
        elevenlabs.save(ai_audio_seg, f"temp/audio0.mp3")

        # creates combined mp3 object
        combined = AudioSegment.from_mp3("temp/audio0.mp3")

        # checks if more segments need to be made
        if len(body_lst) > 1:
            for i, seg in enumerate(body_lst[1:]):
                # saves next audio segments
                ai_audio_seg = elevenlabs.generate(
                   text=seg,
                   voice="Adam",
                   api_key=os.environ['ELEVEN_LABS_KEY']
                )
                elevenlabs.save(ai_audio_seg, f"temp/audio{i + 1}.mp3")

                # combines new segment with combined mp3 object
                combined += AudioSegment.from_mp3(f"temp/audio{i + 1}.mp3")

        combined.export(f"audio/{post}.mp3", format="mp3")
    pass


if __name__ == "__main__":
    main()
