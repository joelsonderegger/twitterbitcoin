# Script: CollectCrypocurrencyData.py
# Authors: Joel Sonderegger

""" This script calculates the correlation between tweets containing 'bearish' or 'bullish' and the bitcoin price
"""

import numpy as np
import csv


# Gets tweets from CSV-File. Returns a list of tweets (of type dict)
def getTweets():

    # create an empty list that will contain all tweets
    tweets = []

    with open('data/twitterData.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:

            tweet = {}
            tweet['created_at'] = row[0]
            tweet['text'] = row[1]

            tweets.append(tweet)

        csvfile.close()


    # return a list of tweets (of type dict)
    return tweets


# Order Tweets by Date and return as list of dicts. For each day there is one dict that contains (1) a date and (2) a list of containing all tweets
# {'date': '23-23-4302', "tweets" : ["bla","bla","bla"]}
def orderTweetsByDay(tweets)
    tweets_ordered_by_day = []

    return tweets_ordered_by_day


def main():

    tweets = getTweets()
    print(tweets)

    tweets_ordered_by_day = orderTweetsByDay(tweets)

    # for each day
    number_of_bea

    # output: daily_bearish_bullish_numbers = [{'day':'23-11-2017', 'bearish': 11, 'bullish': 25}, {'day':'24-11-2017', 'bearish': 15, 'bullish': 21}]

    mystring = "I belive the bitcoin is going up bearish"
    # find tweets that contain 'bearish'
    word = 'bearish'

    if word in mystring: 
        print 'success'


if __name__ == '__main__':
    main()



