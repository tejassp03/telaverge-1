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

    def download_users_profile_picture(self,username):
        self.L.download_profile(username, profile_pic_only=True)

    def download_users_posts_with_periods(self,username):
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        SINCE = datetime(2021, 8, 28)
        UNTIL = datetime(2021, 9, 30)

        for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
            self.L.download_post(post, username)

    def download_hastag_posts(self, hashtag):
        for post in instaloader.Hashtag.from_name(self.L.context, hashtag).get_posts():
            self.L.download_post(post, target='#'+hashtag)

    def get_users_followers(self,user_name):
        '''Note: login required to get a profile's followers.'''
        self.L.login(input("input your username: "), input("input your password: ") )
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("follower_names.txt","a+")
        for followee in profile.get_followers():
            username = followee.username
            file.write(username + "\n")
            print(username)



    def get_users_followings(self,user_name):
        '''Note: login required to get a profile's followings.'''
        self.L.login(input("input your username: "), input("input your password: ") )
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("following_names.txt","a+")
        for followee in profile.get_followees():
            username = followee.username
            file.write(username + "\n")
            print(username)

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

    def get_post_info_csv(self,username):
        with open(username+'.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
            for post in posts:
                print("post date: "+str(post.date))
                print("post profile: "+post.profile)
                print("post caption: "+post.caption)
                print("post location: "+str(post.location))

                posturl = "https://www.instagram.com/p/"+post.shortcode
                print("post url: "+posturl)
                writer.writerow(["post",post.mediaid, post.profile, post.caption, post.date, post.location, posturl,  post.typename, post.mediacount, post.caption_hashtags, post.caption_mentions, post.tagged_users, post.likes, post.comments,  post.title,  post.url ])

                for comment in post.get_comments():
                    writer.writerow(["comment",comment.id, comment.owner.username,comment.text,comment.created_at_utc])
                    print("comment username: "+comment.owner.username)
                    print("comment text: "+comment.text)
                    print("comment date : "+str(comment.created_at_utc))
                print("\n\n")

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
    # cls.get_post_info_csv("ashishchanchlani")\
    comments_data = cls.get_post_comments("googleindia")
    negative_comments = cls.analyze_sentiment(comments_data)

    print(f"Number of negative comments: {len(negative_comments)}")
    print(negative_comments)