# Script: CollectCrypocurrencyData.py
# Authors: Joel Sonderegger

""" This script calculates the correlation between tweets containing 'bearish' or 'bullish' and the bitcoin price
"""

import pandas as pd
import numpy as np
import pprint
import csv
import io


# Gets tweets from CSV-File. Returns a list of tweets (of type dict)
def load_tweets():
    df = pd.read_csv('data/twitterData.csv')

    return df


# Order Tweets by Date and return as list of dicts. For each day there is one dict that contains (1) a date and (2) a list of containing all tweets
# {'date': '23-23-4302', "tweets" : ["bla","bla","bla"]}

def count_tweets_per_hour(tweets):

    # drop the tweet text as the timestamp are enough to count the number of tweets
    tweets.drop('text', axis=1, inplace=True)

    # use create_at as the index of the df tweets
    times = tweets.set_index(pd.DatetimeIndex(tweets['created_at']))

    #group by year, month, day and hour
    grouped_tweets_per_hour = tweets.groupby([times.index.year, times.index.month, times.index.day, times.index.hour]).count()
    
    # set correct index names for Y, M, D, H
    grouped_tweets_per_hour.index = grouped_tweets_per_hour.index.set_names('Y', level=0)
    grouped_tweets_per_hour.index = grouped_tweets_per_hour.index.set_names('M', level=1)
    grouped_tweets_per_hour.index = grouped_tweets_per_hour.index.set_names('D', level=2)
    grouped_tweets_per_hour.index = grouped_tweets_per_hour.index.set_names('H', level=3)

    # set correct column names nr_tweets (replaced value: created_at)
    grouped_tweets_per_hour.rename(columns = {'created_at':'nr_tweets'}, inplace = True)
   
    # output of results
    print(grouped_tweets_per_hour)

    # return df 
    return grouped_tweets_per_hour


def main():

    # load tweets for csv-file
    tweets = load_tweets()

    # count number of tweets per hour
    tweets_per_hour = count_tweets_per_hour(tweets)



if __name__ == '__main__':
    main()



