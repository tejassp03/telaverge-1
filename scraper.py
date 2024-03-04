import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile,islice
from textblob import TextBlob
import csv

import pandas as pd

class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()
        self.L.login('tejassp0303','tejastiger@2003')

    def get_post_comments(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)
        # Limit posts to the 10 latest using islice
        posts = islice(profile.get_posts(), 3)
        comments_data = []
        for post in posts:
            for comment in post.get_comments():
                comments_data.append({
                    'comment_id': comment.id,
                    'username': comment.owner.username,
                    'text': comment.text,
                    'created_at_utc': comment.created_at_utc
                })
        return comments_data


    def analyze_sentiment(self,comments_data):
        df = pd.DataFrame(comments_data)
        df['sentiment'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
        negative_comments = df[df['sentiment'] < 0]
        return negative_comments

if __name__=="__main__":
    cls = GetInstagramProfile()
    # cls.download_users_profile_picture("best_gadgets_2030")
    # cls.download_users_posts_with_periods("best_gadgets_2030")
    # cls.download_hastag_posts("gadgets")
    # cls.get_users_followers("best_gadgets_2030")
    # cls.get_users_followings("best_gadgets_2030")
    # cls.get_post_info_csv("ashishchanchlani")
    # comments_data = cls.get_post_comments("googleindia")
    # negative_comments = cls.analyze_sentiment(comments_data)

    # print(f"Number of negative comments: {len(negative_comments)}")
    # print(negative_comments)