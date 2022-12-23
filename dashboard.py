from visualize import *
from visualize_user import *
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import snscrape.modules.twitter as sntwitter
import pandas as pd

st.write("# WeTweet") 
st.write('_______________________')
st.write("""## How it works""")
st.write("WeTweet is a tool to extract and analyze the Twitter data to get meaningful insights. This tool gives you the graphical representation of the data in the form of a report." 
        " WeTweet can fetch the data of any hashtag or a user profile keeping in mind the conditions like- Date range, location, etc.")

#image
image = Image.open('images/twitter.jpg')
st.image(image)

# Pre-process Data
def preprocess(df):
    df['Hashtags'].fillna('', inplace=True)
    df['Users Mentioned'].fillna('', inplace=True)
    df['Quoted Tweet'].fillna('', inplace=True)
    df['Reply to Tweet Id'].fillna(0, inplace=True)
    df['Reply to User'].fillna('', inplace=True)
    df['Retweeted Tweet'].fillna(0, inplace=True)
    df['Outlinks'].fillna('', inplace=True)
    df['place'].fillna('', inplace=True)
    df['Coordinates'].fillna('', inplace=True)

    # Tweet date
    df['Temp Date'] = df['Date']
    df['Date'] = pd.to_datetime(df['Temp Date']).apply(lambda x: x.date())
    df['Time'] = pd.to_datetime(df['Temp Date']).apply(lambda x: x.time())
    df['Tweet Year'] = df['Date'].apply(lambda x: x.year)
    df.drop('Temp Date', axis=1, inplace=True)

    # User Creation date
    df['Temp Date'] = df['User Created']
    df['User Created Date'] = pd.to_datetime(df['Temp Date']).apply(lambda x: x.date())
    df['User Created Time'] = pd.to_datetime(df['Temp Date']).apply(lambda x: x.time())
    df['User Created Year'] = df['User Created Date'].apply(lambda x: x.year)
    df.drop('Temp Date', axis=1, inplace=True)
    return df

# Fetch Twitter Data
def fetch_data(query_string, type, record_choice):
    # query_string = '(from:TurkeyUrdu)'
    if type == 'profile':
        query_string = '(from:' + query_string + ')'
    tweets_list = []
    limits = record_choice
    df = pd.DataFrame()

    for tweet in sntwitter.TwitterSearchScraper(query_string).get_items():
        try:
            if len(tweets_list) == limits:
                break
            else:
                # appending data to tweets list
                tweets_list.append([tweet.id, tweet.conversationId, tweet.date, tweet.lang, tweet.content, tweet.user.username, tweet.user.id, tweet.user.displayname, 
                tweet.user.description, tweet.user.created, tweet.user.verified, tweet.user.followersCount, tweet.user.friendsCount, tweet.user.location, tweet.hashtags, tweet.mentionedUsers,
                tweet.quotedTweet, tweet.likeCount, tweet.replyCount, tweet.retweetCount, tweet.quoteCount, tweet.inReplyToTweetId, tweet.inReplyToUser, tweet.retweetedTweet, 
                tweet.outlinks, tweet.place, tweet.coordinates, tweet.url])
        except:
            break

    # Creating a dataframe with the tweets list
    tweets_df = pd.DataFrame(tweets_list, columns=["Tweet Id", "Conversation Id", "Date", "Language", "Content", "Username", "User Id", "User Display Name", 
    "User Description", "User Created", "User Verified", "User Followers", "User Following", "User Location", "Hashtags", "Users Mentioned",
    "Quoted Tweet", "Total Likes", "Total Replies", "Total Retweets", "Total Quotes", "Reply to Tweet Id", "Reply to User", "Retweeted Tweet", "Outlinks", "place",
    "Coordinates", "Tweet Url"])

    # tweets_df.to_csv("data_fifa.csv", encoding="UTF-8", index=False)
    # Pre-processing data
    tweets_df = preprocess(tweets_df)
    return tweets_df

# Download CSV
@st.cache
def download_df(df):
    return df.to_csv().encode('utf-8')

# Visualize General Data
def visualize(data_df):
    st.title('Twitter Data Analysis')
    # path = 'data/' + keyword + "_data.json"
    # data_df = pd.read_json(path, lines=True)

    # Timline graph of the keyword
    try:
        timeline_graph = timeline(data_df)
        if timeline_graph != '':
        # Tweets Timeline Plot!
        # print(type(timeline_graph))
            st.write(timeline_graph)
        else:
            pass
    except:
        pass

    # # Username Graph
    # users_moslty_interacted(data_df, keyword)

    # # Hashtags Graph
    hashtags_graph = hashtags_used(data_df)
    st.subheader("Hashtags Used in the Tweets")
    st.write(hashtags_graph)

    # Tweets per year
    tweets_yearly_graph = tweets_per_year(data_df)
    st.subheader("Tweets Done Per Year")
    st.write(tweets_yearly_graph)

    # Accounts Tweeted Mostly
    accounts_tweeted_graph = accounts_tweeted(data_df)
    st.subheader("Accounts Majorly Tweeted")
    st.write(accounts_tweeted_graph)

    # Accounts Timeline
    accounts_timeline_graph = accounts_timeline(data_df)
    st.subheader("Accounts Creation Timeline")
    st.write(accounts_timeline_graph)

    # Verified Accounts
    verified_acc_graph = verified_accounts(data_df)
    st.subheader("Verified Accounts Tweeted")
    st.write(verified_acc_graph)

    # Verified Accounts Percentage
    verified_acc_prop_graph = verified_accounts_per(data_df)
    st.subheader("Percentage of Verified / Non Verified Account")
    st.write(verified_acc_prop_graph)

    accounts_mentioned_graph = accounts_mentioned(data_df)
    st.subheader("Accounts Mostly Mentioned")
    st.write(accounts_mentioned_graph)

    languages_used_graph = languages_used(data_df)
    st.subheader("Top Languages Used in the Tweets")
    st.write(languages_used_graph)

    # Most Liked Tweets
    most_liked_tweets_tab = most_liked_tweets(data_df)
    st.subheader("Most Liked Tweets")
    st.table(most_liked_tweets_tab)

    # Most Retweeted Tweets
    most_retweeted_tweets_tab = most_retweeted_tweets(data_df)
    st.subheader("Most Retweeted Tweets")
    st.table(most_retweeted_tweets_tab)

    # Download Button
    st.caption("Click the below button to download the data.")
    csv = download_df(data_df)
    st.download_button(
        label="Download Data",
        data=csv,
        file_name='data.csv',
        mime='text/csv',
    )

# Visualize User Data
def visualize_user(data_df):
    st.title('Twitter Data Analysis')
    # path = 'data/' + keyword + "_data.json"
    # data_df = pd.read_json(path, lines=True)

    # Timline graph of the keyword
    try:
        timeline_graph = timeline(data_df)
        if timeline_graph != '':
        # Tweets Timeline Plot!
        # print(type(timeline_graph))
            st.write(timeline_graph)
        else:
            pass
    except:
        pass

    # # Username Graph
    # users_moslty_interacted(data_df, keyword)

    # # Hashtags Graph
    hashtags_graph = hashtags_used(data_df)
    st.subheader("Hashtags Used in the Tweets")
    st.write(hashtags_graph)

    # Tweets per year
    tweets_yearly_graph = tweets_per_year(data_df)
    st.subheader("Tweets Done Per Year")
    st.write(tweets_yearly_graph)

    accounts_mentioned_graph = accounts_mentioned(data_df)
    st.subheader("Accounts Mostly Mentioned")
    st.write(accounts_mentioned_graph)

    # Most Liked Tweets
    most_liked_tweets_tab = most_liked_tweets(data_df)
    st.subheader("Most Liked Tweets")
    st.table(most_liked_tweets_tab)

    # Most Retweeted Tweets
    most_retweeted_tweets_tab = most_retweeted_tweets(data_df)
    st.subheader("Most Retweeted Tweets")
    st.table(most_retweeted_tweets_tab)

    # Download Button
    st.caption("Click the below button to download the data.")
    csv = download_df(data_df)
    st.download_button(
        label="Download Data",
        data=csv,
        file_name='data.csv',
        mime='text/csv',
    )

# Siderbar
st.sidebar.image("images/dfrac_logo.png", width=100)
st.sidebar.header("# Fetch Tweets")
query_type = st.sidebar.radio("Choose the type of your query!", ('General', 'Profile'), help="General- General category includes search queries for hashtags, profile")

# General query
if query_type == 'General':
    st.write("""## General Query""")
    query = st.text_input('Please enter you query here', help="Enter your query to analyze the data")
    record_choice = st.radio(
                    "How many number of records you want to fetch?",
                    (1000, 5000, 10000, 50000), help="IMPORTANT: Resquesting higher number of records can take more time to fetch data. 50,000 records can take upto 1 hour to fetch data.")
    if st.button("Search"):
        if query.strip != '':
            load_screen = 1
            while load_screen == 1:
                with st.spinner('Fetching Data'):
                    type = "general"
                    data_df = fetch_data(query, type, record_choice)
                    load_screen = 0
            visualize(data_df)

        else:
            st.error("Please write a query to search!")
else:
    # Profile Query
    st.write("""## Profile Query""")
    query = st.text_input('Please enter the profile of the user', help='Enter the username of the user to analyze the data')
    record_choice = st.radio(
                    "How many number of records you want to fetch?",
                    (1000, 5000, 10000, 50000), help="IMPORTANT: Resquesting higher number of records can take more time to fetch data. 50,000 records can take upto 1 hour to fetch data.")
    if st.button("Search"):
        if query.strip != '':
            load_screen = 1
            while load_screen == 1:
                with st.spinner('Fetching Data, Please Wait!'):
                    type = "profile"
                    data_df = fetch_data(query, type, record_choice)
                    load_screen = 0
            visualize_user(data_df)

        else:
            st.error("Please write a query to search!")