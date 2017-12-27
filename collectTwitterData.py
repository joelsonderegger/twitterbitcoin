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
import pprint
from pathlib import Path

# Import smtplib for the email sending function
import smtplib



#consumer key, consumer secret, access token, access secret.
ckey="ANR2xCLJwM24NirkkFLlurkJY"
csecret="KFAiqNSVErT7QzAlBYSkUmhGaCoEJJLnfmnG0x7SJJbDT2Qe1k"
atoken="933214447291604992-xWBg0xEPzsWvrXSVTe5mWEr5o4SVH2n"
asecret="DRJUfwWxk8MqKUZILnq8zu0pcsKahtTWZCKB64C822VQv"

# function to send email with error
def send_email(sbjt, msg):
    fromaddr = 'twitterbitcoinanalysis@gmail.com'
    toaddrs = 'joel.sonderegger@googlemail.com'
    bodytext = 'From: %s\nTo: %s\nSubject: %s\n\n%s' %(fromaddr, toaddrs, sbjt, msg)
   
    # Credentials (if needed)
    username = 'twitterbitcoinanalysis@gmail.com'
    password = 'wNvfuXAiek9i' 
  
    # The actual mail sent
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, bodytext)
    server.quit()


class listener(StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded_tweet = json.loads(data)
        
        # Exception handling for KeyError. LookupError is the base class for the exceptions that are raised when a key or index used on a mapping or sequence is invalid: IndexError, KeyError
        try:
            # prints data for one tweet
            print("===========")

            # check if text has key created_at (there where tweets without crashing the program)
            if 'created_at' in decoded_tweet:

                # defines where the data is saved. Opening the file 'a' stands for appending
                tweets_file = open('data/twitterData.csv', 'a')


                # gets relevant data from data object
                created_at = decoded_tweet['created_at']
                text = decoded_tweet['text'].encode('utf-8')
            
            
                # Create a row that contains all relevant twitter data
                tweet = [created_at, text]
                print(tweet)

                # print out what is saved to the file
                #pp = pprint.PrettyPrinter(indent=4)
                #pprint.pprint(tweet)

                # appends the tweet to the  csv-file
                with tweets_file:
                   writer = csv.writer(tweets_file)
                   writer.writerow(tweet)
                tweets_file.close()

        except LookupError:

            # The error message
            error_msg = 'LookupError for tweet with content (var decoded_tweet):\n' + text

            # send error email
            send_email('Twitter Collector Script Error:', error_msg)

            # print out error message
            print(error_msg)

            # write the tweet data into a log file
            error_log_file = open('data/tweet_collection_error_log.csv', 'a')
            with tweets_file:
               writer = csv.writer(error_log_file)
               writer.writerow(decoded_tweet)
            error_log_file.close()
            pass

        # This will catch any exception
        except:
             # The error message
            error_msg = 'unexpected error for tweet with content (var decoded_tweet):\n' + text + '\n\n' + "system error log:\n" + sys.exc_info()[0]

            # send error email
            send_email('Twitter Collector Script Error:', error_msg)

            # print out error message
            print(error_msg)
            pass

        return(True)

    def on_error(self, status):
        print(status)


# create csv file with headers with it does not exist in data folder
def create_tweet_csv():
    print("Checking if csv-file for collecting tweets exists...")

     # defines where the csv should be.
    tweets_file = Path('data/twitterData.csv')

    if tweets_file.is_file():
        print("csv-file for collecting tweets exists.")
        # file exists
        return(False)
    else:
        print("csv-file for collecting tweets does not exists yet.")
        
        # opens the csv-file. 'w' stands for write
        tweets_file = open('data/twitterData.csv', 'w')

        # header for csv-file
        header = ["created_at", "text"]

        # header for csv-file
        with tweets_file:
            writer = csv.writer(tweets_file)
            writer.writerow(header)
        tweets_file.close()

        print("csv-file with header successfully created.")
        return(True)


# Main function
def main():

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    # create csv file with headers with it does not exist in data folder
    create_tweet_csv()

    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["bitcoin"])


if __name__ == '__main__':
    main()

