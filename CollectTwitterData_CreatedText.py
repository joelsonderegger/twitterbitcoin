# Script: CollectTwitterData.py
# Authors: Alen

""" This script gets tweets for a defined period that contain the word bitcoin.
    The output is a csv-file with the tweets.
 To use twitter APIs you have to open a twitteraccount on twitter application
for the api credentials. A good tutorial can be found under
https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
"""

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import csv

#consumer key, consumer secret, access token, access secret.
ckey="ANR2xCLJwM24NirkkFLlurkJY"
csecret="KFAiqNSVErT7QzAlBYSkUmhGaCoEJJLnfmnG0x7SJJbDT2Qe1k"
atoken="933214447291604992-xWBg0xEPzsWvrXSVTe5mWEr5o4SVH2n"
asecret="DRJUfwWxk8MqKUZILnq8zu0pcsKahtTWZCKB64C822VQv"


class listener(StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decodedTweet = json.loads(data)
         # prints data for one tweet
        print("===========")

        # defines where the data is saved. Opening the file 'a' stands for appending
        saveFile = open('data/twitterData.csv', 'a')

        # gets relevant data from data object
        created_at = decodedTweet['created_at']
        text = decodedTweet['text'].encode('utf-8')

        # Create a row that contains all relevant twitter data
        tweet = [created_at, text]

        # print out what is saved to the file
        print(tweet)

        # appends the tweet to the  csv-file
        with saveFile:
           writer = csv.writer(saveFile)
           writer.writerow(tweet)
        saveFile.close()
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["bitcoin"])