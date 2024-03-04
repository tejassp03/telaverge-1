import streamlit as st
import json
from facebook import get_facebook_posts, get_facebook_comments, analyze_sentiment
from twitter_scraper_selenium import scrape_profile_with_api
from scraper import GetInstagramProfile
from textblob import TextBlob

# Function to analyze sentiment of comments
def analyze_sentiment(comments_data):
    negative_comments = []
    for comment in comments_data:
        sentiment_score = TextBlob(comment).sentiment.polarity
        if sentiment_score < 0:
            negative_comments.append({'text': comment, 'sentiment': sentiment_score})
    return negative_comments

def extract_full_text(data):
    texts = []

    # Recursive function to traverse the JSON data
    def traverse(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "full_text":
                    texts.append(value)
                else:
                    traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)
    return texts

# Function to get Twitter tweets
def get_twitter_tweets(profile_name):
    scrape_profile_with_api(profile_name, output_filename=profile_name, tweets_count=5)
    with open(f"{profile_name}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        tweets = extract_full_text(data)
    return tweets

# Streamlit app title and description
st.title("Social Media Sentiment Analysis")
st.write("Select the social media platform and enter the profile name to analyze its content.")

# Sidebar for selecting social media platform
platform = st.sidebar.radio("Select Platform", ("Facebook", "Twitter","Instagram"))

if platform == "Facebook":
    # Input field for the page name
    page_name = st.text_input("Enter the Facebook page name:")

    # Button to trigger the analysis
    if st.button("Analyze Facebook Comments"):
        if not page_name:
            st.error("Please enter a valid page name.")
        else:
            # Show loading state
            with st.spinner("Loading... This may take up to 1 minute."):
                # Get post IDs
                post_ids = get_facebook_posts(page_name)

                # Get comments for each post
                all_comments = get_facebook_comments(post_ids)

                # Analyze sentiment of comments
                negative_comments = analyze_sentiment(all_comments)

                # Display negative comments
                if negative_comments:
                    st.header("Negative Comments")
                    for idx, comment in enumerate(negative_comments, start=1):
                        st.write(f"{idx}. **Sentiment Score:** {comment['sentiment']:.2f}, **Comment:** {comment['text']}")
                else:
                    st.warning("No negative comments found.")
elif platform == "Instagram":
    # Input field for the page name
    page_name = st.text_input("Enter the Instagram page name:")

    # Button to trigger the analysis
    if st.button("Analyze Instagram Comments"):
        if not page_name:
            st.error("Please enter a valid page name.")
        else:
            # Show loading state
            with st.spinner("Loading... This may take up to 1 minute."):
                # Get post IDs
                incls = GetInstagramProfile()
                comm_ids = incls.get_post_comments(page_name)
                # Analyze sentiment of comments
                comment_texts = [comment['text'] for comment in comm_ids]
                negative_comments = analyze_sentiment(comment_texts)
                # Display negative comments
                if negative_comments:
                    st.header("Negative Comments")
                    for idx, comment in enumerate(negative_comments, start=1):
                        st.write(f"{idx}. **Sentiment Score:** {comment['sentiment']:.2f}, **Comment:** {comment['text']}")
                else:
                    st.warning("No negative comments found.")

elif platform == "Twitter":
    # Input field for the Twitter profile name
    twitter_profile_name = st.text_input("Enter the Twitter profile name:")

    # Button to trigger the analysis
    if st.button("Analyze Twitter Tweets"):
        if not twitter_profile_name:
            st.error("Please enter a valid Twitter profile name.")
        else:
            # Show loading state
            with st.spinner("Loading... This may take up to 1 minute."):
                # Get tweets
                tweets = get_twitter_tweets(twitter_profile_name)

                # Analyze sentiment of tweets
                negative_tweets = analyze_sentiment(tweets)

                # Display negative tweets
                if negative_tweets:
                    st.header("Negative Tweets")
                    for idx, tweet in enumerate(negative_tweets, start=1):
                        st.write(f"{idx}. **Sentiment Score:** {tweet['sentiment']:.2f}, **Tweet:** {tweet['text']}")
                else:
                    st.warning("No negative tweets found.")
