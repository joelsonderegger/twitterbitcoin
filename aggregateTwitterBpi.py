# Script: collectCrypocurrencyData.py
# Authors: Joel Sonderegger

""" This script calculates the correlation between tweets containing 'bearish' or 'bullish' and the bitcoin price
"""

import pandas as pd
import numpy as np
import pprint
import csv
import io

from datetime import datetime
from dateutil.parser import parse

# required for logarithmic function
import math

# Gets tweets from CSV-File. Returns a data frame with tweets
def load_tweets():
    df = pd.read_csv('data/20171223_0056_twitterData.csv')
    return df

# Gets bpi data from CSV-File. Returns a data frame with bpi data
def load_bpi():
    bpi_data = pd.read_csv('data/bpi.csv')

    # drop not needed columns
    bpi_data.drop('average', axis=1, inplace=True)
    bpi_data.drop('high', axis=1, inplace=True)
    bpi_data.drop('low', axis=1, inplace=True)

    # create new column 'close'. The close price is the open price of the previous hour
    bpi_data['close'] = bpi_data['open']
    bpi_data['close'] = bpi_data['close'].shift(-1)
    
    # Set time as DataFrame index.
    times = bpi_data.set_index(pd.DatetimeIndex(bpi_data['time']))
    
    bpi_data = bpi_data.set_index([times.index.year, times.index.month, times.index.day, times.index.hour])
 
    # set correct index names for Y, M, D, H
    bpi_data.index = bpi_data.index.set_names('Y', level=0)
    bpi_data.index = bpi_data.index.set_names('M', level=1)
    bpi_data.index = bpi_data.index.set_names('D', level=2)
    bpi_data.index = bpi_data.index.set_names('H', level=3)

    return bpi_data

# Enriches BPI data frame with first difference and log first difference
def first_difference_bpi(bpi_df):

    # assigning the variable here to check later if there is a 'previous' btc close price.
    prev_btc_close = None

    for index, row in bpi_df.iterrows():
        
        # get btc closing price for index
        this_btc_close = bpi_df.get_value(index, 'close', takeable=False)

        # prev_tw = DataFrame.get_value(index, 'close', takeable=False)
        if prev_btc_close is not None:

            # calculate the first difference for the btc closing price
            first_difference_btc_close = this_btc_close - prev_btc_close
            bpi_df.set_value(index, 'df_btc_close', first_difference_btc_close, takeable=False)

            # calculate the log first difference for the btc closing price
            log_first_difference_btc_close = math.log(this_btc_close) - math.log(prev_btc_close)
            bpi_df.set_value(index, 'log_df_btc_close', log_first_difference_btc_close, takeable=False)

        # set prev_tw for nex iteration
        prev_btc_close = this_btc_close

    return bpi_df

# Enriches tweets_per_hour data frame with first difference and log first difference
def first_difference_tweets(tweets_per_hour):

    # assigning the variable here to check later if there is a 'previous' nr of tweets.
    prev_nr_of_tweets = None

    for index, row in tweets_per_hour.iterrows():
        
        # get nr of tweets for index
        this_nr_of_tweets = tweets_per_hour.get_value(index, 'nr_tweets', takeable=False)

        # prev_tw = DataFrame.get_value(index, 'close', takeable=False)
        if prev_nr_of_tweets is not None:

            # calculate the first difference for the btc closing price
            first_difference_nr_of_tweets = this_nr_of_tweets - prev_nr_of_tweets
            tweets_per_hour.set_value(index, 'df_nr_of_tweets', first_difference_nr_of_tweets, takeable=False)

            # calculate the log first difference for the btc closing price
            log_first_difference_nr_of_tweets = math.log(this_nr_of_tweets) - math.log(prev_nr_of_tweets)
            tweets_per_hour.set_value(index, 'log_df_nr_of_tweets', log_first_difference_nr_of_tweets, takeable=False)

        # set prev_tw for nex iteration
        prev_nr_of_tweets = this_nr_of_tweets

    return tweets_per_hour

# Order Tweets by Date and return as list of dicts. For each day there is one dict that contains (1) a date and (2) a list of containing all tweets
# {'date': '23-23-4302', "tweets" : ["bla","bla","bla"]}
def count_tweets_per_hour(tweets):

    # drop the tweet texts as the timestamp are enough to count the number of tweets
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
    
    # return df 
    return grouped_tweets_per_hour


def generate_csv(df_merged):
    # This is the header for the list that contains nr of tweets and the bpi closing price for every hour
    header = ['time', 'nr_of_tweets', 'df_nr_of_tweets', 'log_df_nr_of_tweets', 'bpi_closing_price', 'df_bpi_closing_price', 'log_df_bpi_closing_price']

    # creating list that will contain hourly data
    data_array = []
    
    # loop through df_merged and appends a row that contains data for one hour to the data_array
    for index, row in df_merged.iterrows():
        hourly_array = [row['time'], row['nr_tweets'], row['df_nr_of_tweets'], row['log_df_nr_of_tweets'], row['close'], row['df_btc_close'], row['log_df_btc_close']]
        data_array.append(hourly_array)

    # addind the header to the list which contains contains nr of tweets and the bpi closing price for every hour
    data_array = [header] + data_array

    # Defines the path where the data should be written
    csvFile = open('data/nr_of_tweets_bpi_closing_price.csv', 'w')

    # write the the list which contains nr of tweets and the bpi closing price for every hour (inkl. header) to csv-file
    with csvFile:
       writer = csv.writer(csvFile)
       writer.writerows(data_array)

    return None


def main():

    # load tweets from csv-file
    tweets = load_tweets()

    # load bitcoin price index (bpi) data from csv-file
    bpi_data = load_bpi()

    # enrich BPI data frame with first difference and log first difference
    bpi_data = first_difference_bpi(bpi_data)
    print(bpi_data)

    # count number of tweets per hour
    #print('Counting the number of tweets. This can take some minutes...')
    #tweets_per_hour = count_tweets_per_hour(tweets)
    
    # enrich tweets_per_hour data frame with first difference and log first difference
    #tweets_per_hour = first_difference_tweets(tweets_per_hour)

    # merge number of tweets per hour with bitcoin price index (bpi) data
    #df_merged = tweets_per_hour.join(bpi_data, how='left')

    #print(df_merged)
    # Write out to csv
    #generate_csv(df_merged)

if __name__ == '__main__':
    main()



