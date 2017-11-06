import urllib2
import numpy as np
import json
import datetime

startDate = datetime.datetime.strptime('01/11/2017','%d/%m/%Y').date()
endDate = datetime.datetime.strptime('05/11/2017','%d/%m/%Y').date()


# Get historical Bitcoin Price Index data. The index is returned in USD.
def getBPI(startDate, endDate):
	startDateString = startDate.strftime('%Y-%m-%d')
	endDateString = endDate.strftime('%Y-%m-%d')

	# API Infos: https://www.coindesk.com/api/
	r = urllib2.urlopen("https://api.coindesk.com/v1/bpi/historical/close.json?start=" + startDateString + "&end=" + endDateString).read()
	r = json.loads(r)["bpi"]


	bpi = {}

	for day in r:

		# add a day to the bpi dict
		bpi[day] = {'price': r.get(day)}

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

		print(str(prevDayPriceStorage) + " - " + str(value['price']))

		enrichedBPI[key] = {'price': value['price'], 'changeInPercentage': changeInPercentage, 'changeInAbsolute': changeInAbsolute }

		# save price for following day price caluclations
		prevDayPriceStorage = value['price']
	return enrichedBPI

# Get BPI for a specific period
bpi = getBPI(startDate, endDate)

# Calculate some values for BPI (e.g. change in percentage)
bpiEnriched = getEnrichedBPI(bpi)


print(bpiEnriched)