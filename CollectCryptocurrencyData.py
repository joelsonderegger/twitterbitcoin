
# Script: CollectCrypocurrencyData.py
# Authors: Joel Sonderegger

""" This script gets crypocurrency data.
	The output is a csv-file with the crypocurrency prices.
"""


import urllib2
import numpy as np
import json
import datetime
import csv


startDate = datetime.datetime.strptime('01/11/2017','%d/%m/%Y').date()
endDate = datetime.datetime.strptime('22/11/2017','%d/%m/%Y').date()


# Get historical Bitcoin Price Index data. The index is returned in USD.
def getBPI(startDate, endDate):
	startDateString = startDate.strftime('%Y-%m-%d')
	endDateString = endDate.strftime('%Y-%m-%d')

	# API Infos: https://www.coindesk.com/api/
	r = urllib2.urlopen("https://api.coindesk.com/v1/bpi/historical/close.json?start=" + startDateString + "&end=" + endDateString).read()
	r = json.loads(r)["bpi"]

	bpi = {}

	for day in r:
		# add a day to the bpi dict. However correct order by date is not garanteed. 
		bpi[day] = {'price': r.get(day)}

		print day

	# order the list of bpi by date. starting with the oldest date, ending with the most recent date.
	print(sorted(bpi,key=lambda x:datetime.datetime.strptime(x[1],"%Y-%m-%d")))
	
	
	return bpi


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
def generateCSV(bpi):

	bpi_list = []

	for key, value in bpi.iteritems():
	    temp = [key,value['price']]
	    bpi_list.append(temp)

	# This is the final array which contains the BPI data that is outputed in the csv-file
	bpiData = [['Date', 'Price'], ['11/12/2017', 134.00], ['11/12/2017', 134.00], ['11/12/2017', 134.00]]  

	# Defines to with file the data should be writen
	csvFile = open('data/bpi.csv', 'w')  

	# write the bpiData to csv-file
	with csvFile:  
	   writer = csv.writer(csvFile)
	   writer.writerows(bpi_list)
	return None

# Begin the Python script that will do the workdef main():
def main():
	#Get BPI for a specific period
	bpi = getBPI(startDate, endDate)

	# Calculate some values for BPI (e.g. change in percentage)
	bpiEnriched = getEnrichedBPI(bpi)

	

	generateCSV(bpi)


if __name__ == '__main__':
	main()

