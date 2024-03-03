import facebook_scraper as fs
import requests
import json
import pandas as pd
from textblob import TextBlob

from facebook_page_scraper import Facebook_scraper

def get_facebook_posts(page_name):
    posts_count = 3
    browser = "chrome"
    proxy = "tejashurricane@gmail.com:TejasTiger@2003@IP:PORT" #if proxy requires authentication then user:password@IP:PORT
    timeout = 20 #600 seconds
    headless = True
    meta_ai = Facebook_scraper(page_name, posts_count, browser, proxy=proxy, timeout=timeout, headless=headless,)
    json_data = meta_ai.scrap_to_json()
    json_dict = json.loads(json_data)

    # Extract and print all post IDs
    post_ids = list(json_dict.keys())
    return post_ids


def get_facebook_comments(post_ids):
    all_comments = []  
    for post_id in post_ids:
    
        POST_ID = post_id

        MAX_COMMENTS = 10
        try:
            # get the post (this gives a generator)
            gen = fs.get_posts(
                post_urls=[POST_ID],
                options={"comments": MAX_COMMENTS, "progress": True}
            )

            # take 1st element of the generator which is the post we requested
            post = next(gen)

            # extract the comments part
            comments = post['comments_full']
            comment_texts = [comment['comment_text'] for comment in comments]
            all_comments.extend(comment_texts)
            # process comments as you want...
            # for comment in comments:

            #     # e.g. ...print them
            #     print(comment)

            #     # e.g. ...get the replies for them
            #     for reply in comment['replies']:
            #         print(' ', reply)
        except Exception as e:
            print(f"Error fetching comments for post ID {post_id}: {e}")
            continue
    return all_comments

def analyze_sentiment(comments_data):
    negative_comments = []
    for comment in comments_data:
        sentiment_score = TextBlob(comment).sentiment.polarity
        if sentiment_score < 0:
            negative_comments.append({'text': comment, 'sentiment': sentiment_score})
    return negative_comments

# page_name = "Google"
# post_ids = get_facebook_posts(page_name)
# all_comments = get_facebook_comments(post_ids)
# negative_comments = analyze_sentiment(all_comments)

# for comment in negative_comments:
#     print(comment)
