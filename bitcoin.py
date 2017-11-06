import urllib2
import numpy as np
import json
import datetime

startDate = datetime.datetime.strptime('01/11/2017','%d/%m/%Y').date()
endDate = datetime.datetime.strptime('05/11/2017','%d/%m/%Y').date()

def getBPI(startDate, endDate):
	startDateString = startDate.strftime('%Y-%m-%d')
	endDateString = endDate.strftime('%Y-%m-%d')

	# API Infos: https://www.coindesk.com/api/
	r = urllib2.urlopen("https://api.coindesk.com/v1/bpi/historical/close.json?start=" + startDateString + "&end=" + endDateString).read()

	bpi = json.loads(r)["bpi"]
	return bpi

# Get BPI for a specific period
bpi = getBPI(startDate, endDate)

print(json.dumps(bpi, sort_keys=True, indent=4))