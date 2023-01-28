import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
import datetime
from datetime import date
import time

st.set_page_config(
    page_title="Twitte")

st.header("""
Twitter Scrapping:
""")

today=date.today()

search_radio = st.radio('Type of search',['Username', 'hashtag', 'Messages'])
search_type=''
if search_radio=="Username":
    Search_type="from"
elif search_radio=="hashtag":
    search_type="#"
else:
    search_type=" "

NAME = st.text_input('What do you want to search for?')
count = st.number_input('Enter the limit')
start_date=st.date_input('Enter the start date',datetime.date(2022, 1, 1))
end_date=st.date_input('Enter the end date',today)

csv = st.radio("Download option", ['CSV', 'Json', 'Export'])

count = int(count)
submit_button = st.button(label='Search')

tweets_list1 = []

if submit_button:
    for i , tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_type}:{NAME} since:{start_date} until:{end_date}').get_items()):
        if i > count-1:
            break
        tweets_list1.append(
            [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount,
             tweet.sourceLabel, tweet.user.location])
        tweet_df = pd.DataFrame(tweets_list1, columns=["Date", "Id", "Content", "Username", "LikeCount", "RetweetCount",
                                                       "SourceLabel", "Location"],index=None)

    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1)
    st.dataframe(tweet_df)
    st.balloons()


    st.success("you have Extracted the data ")

    if csv == "CSV":
        file_converted = tweet_df.to_csv()
        st.download_button(
            label="Download data as CSV",
            data=file_converted,
            file_name=f'{NAME} Tweets.csv',
            mime='text/csv',
        )
    elif (csv == 'Json'):
        file_converted = tweet_df.to_json()
        st.download_button(
            label="Download data as json",
            data=file_converted,
            file_name=f'{NAME} Tweets.json',
            mime="application/json",
        )
    elif csv == "Export":
        export_button = st.button(label="Export")
        now = datetime.datetime.now()
        client = pymongo.MongoClient("mongodb+srv://dhivvyan:12345@cluster0.zyyppdj.mongodb.net/?retryWrites=true&w=majority")
        db = client.Data_Scraped_in_twitter
        records = db.Data
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_type}:{NAME}  since:{start_date} until:{end_date}').get_items()):
            if i > count - 1:
                break
            tweets_list1.append(
                [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount,
                 tweet.sourceLabel, tweet.user.location])
            tweet_df = pd.DataFrame(tweets_list1,
                                    columns=["Date", "Id", "Content", "Username", "LikeCount", "RetweetCount",
                                             "SourceLabel", "Location"], index=None)
            l = {"Scraped_Name": NAME, "Time": now, "Scraped_data": [
                    {"Date_Time": tweet.date, "Tweet_ID": tweet.id, "Tweet_content": tweet.content,
                     "Username": tweet.user.username,
                     "Like Count": tweet.likeCount, "ReTweet Count": tweet.retweetCount, "Source": tweet.sourceLabel,
                     "Location": tweet.user.location}]}
            records.insert_one(l)
        st.success("Data has uploaded in Mongodb Server")

