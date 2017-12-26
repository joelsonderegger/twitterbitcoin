
# Script: CollectCrypocurrencyData.py
# Authors: Joel Sonderegger

""" This script gets crypocurrency data.
    The output is a csv-file with the crypocurrency prices.
"""



import numpy as np
import json
import datetime
import csv

# library for pretty printing
import pprint

# libraries required for bitcoinaverage api
import hashlib
import hmac
import requests
import time

secret_key = 'ZTIyNDc2YjE2NmViNGZmMTllZGRkYzM2YWM4MWY4NTk4NTFjZjNiOTI2ZTY0ODQ0OTQzMWNmNzE0ZTU0ODU0YQ'
public_key = 'NzhlNjI2YjY2MTI2NGEzZmEwN2U2ZDExZGY4NDZiNzk'
timestamp = int(time.time())
payload = '{}.{}'.format(timestamp, public_key)
hex_hash = hmac.new(secret_key.encode(), msg=payload.encode(), digestmod=hashlib.sha256).hexdigest()
signature = '{}.{}'.format(payload, hex_hash)

# Get daily bitcoin price index (BPI) data from bitcoinaverage's API
def getHourlyBPI():
    url = 'https://apiv2.bitcoinaverage.com/indices/global/history/BTCUSD?period=monthly&?format=json'
    headers = {'X-Signature': signature}
    result = requests.get(url=url, headers=headers)

    bpi_data = result.json()

    return bpi_data

# not used so far
def getEnrichedBPI(bpi):
    enrichedBPI = {}
    prevDayPriceStorage = 0

    for key, value in bpi.items():
        
        changeInAbsolute = value['price'] - prevDayPriceStorage

        # prevent a division by 0 (would happen on first day)
        if (prevDayPriceStorage != 0):
            changeInPercentage = (changeInAbsolute / prevDayPriceStorage) * 100
        else:
            changeInPercentage = 0


        enrichedBPI[key] = {'price': value['price'], 'changeInPercentage': changeInPercentage, 'changeInAbsolute': changeInAbsolute }

        # save price for following day price caluclations
        prevDayPriceStorage = value['price']

    return enrichedBPI


# Generate the output in form of a CSV-File. Takes in a JSON with BPI data.
def generateCSV(bpi_data):
    
    # This is the header for the list which will contain all bpi data
    header = ['time', 'average', 'high', 'low', 'open']

    # creating list that will contain all bpi data
    bpi_data_array = []
    

    # loop through bpi_data(json) and create a list(day_array) which is appended to the list that contains all bpi data(bpi_data_array)
    for day in bpi_data:
        day_array = [day['time'],day['average'],day['high'],day['low'],day['open']]
        
        bpi_data_array.append(day_array)

    # reversing the list of daily bitcoin data so the list starts with the oldest entry and ends with the most recent
    bpi_data_array.reverse()

    # addind the header to the list which contains all bpi data
    bpi_data_array = [header] + bpi_data_array

    # Defines the path where the data should be written
    csvFile = open('data/bpi.csv', 'w')

    # write the the list which contains all bpi data (bpi_data_array) to the csv-file
    with csvFile:
       writer = csv.writer(csvFile)
       writer.writerows(bpi_data_array)

    # (bpi_data_array) - 1 because we don't want to count the header
    print("Added " + str(len(bpi_data_array)-1) + " entries to data/bpi.csv")

    return None

# Begin the Python script that will do the workdef main():
def main():
    # Get daily bitcoin price index (BPI) data
    bpi_data = getHourlyBPI()

    # Generate the output in form of a CSV-File
    generateCSV(bpi_data)


if __name__ == '__main__':
    main()

