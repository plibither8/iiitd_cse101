# Name : Mihir Chaturvedi
# Roll No : 2019061
# Group : A-7

from datetime import datetime
from urllib.request import urlopen

ENCODING = 'utf-8'
BASE_URL = 'https://api.exchangeratesapi.io'

def getLatestRates():
	""" Returns: a JSON string that is a response to a latest rates query.

	The Json string will have the attributes: rates, base and date (yyyy-mm-dd).
	"""

	URL = f'{BASE_URL}/latest'
	response = urlopen(URL).read().decode(ENCODING)
	return response

def changeBase(amount, currency, desiredCurrency, date):
	""" Outputs: a float value f.
	"""

	URL = f'{BASE_URL}/{date}'
	response = urlopen(URL).read().decode(ENCODING)

	def get_float(code):
		str_start_index = response.find(code) + 5
		str_end_index = response.find(',', str_start_index)

		raw_val = response[str_start_index:str_end_index]
		if raw_val[len(raw_val) - 1] == '}':
			raw_val = raw_val[:-1]

		return(float(raw_val))

	curr_val = get_float(currency)
	des_curr_val = get_float(desiredCurrency)

	converted_val = des_curr_val / curr_val * amount
	return(converted_val)

def printAscending(json):
	""" Output: the sorted order of the Rates 
		You don't have to return anything.
	
	Parameter:
	json: a json string to parse
	"""

	rates_start_index = 10
	rates_end_index = -35
	refined_rates_str = json[rates_start_index:rates_end_index]

	sorted_rates = []
	unsorted_rates_raw_list = refined_rates_str.split(',')

	for rate_str in unsorted_rates_raw_list:
		code, amount = rate_str.split(':')
		code = code[1:-1]
		amount = float(amount)

		sorting_index = 0
		sorted_rates_length = len(sorted_rates)
		while(sorting_index < sorted_rates_length and sorted_rates[sorting_index][1] < amount):
			sorting_index += 1

		sorted_rates.insert(sorting_index, [code, amount])

	for rate in sorted_rates:
		print(f'1 Euro = {rate[1]} {rate[0]}')

def extremeFridays(startDate, endDate, currency):
	""" Output: on which friday was currency the strongest and on which was it the weakest.
		You don't have to return anything.
		
	Parameters: 
	stardDate and endDate: strings of the form yyyy-mm-dd
	currency: a string representing the currency those extremes you have to determine
	"""

	URL = f'{BASE_URL}/history?start_at={startDate}&end_at={endDate}'
	response = urlopen(URL).read().decode(ENCODING)

	rates_start_index = 10
	rates_end_index = -62

	a = response[rates_start_index:rates_end_index].split('},')
	for b in a:
		print(b)
		print()

extremeFridays('2019-08-03', '2019-08-07', 0)


def findMissingDates(startDate, endDate):
	""" Output: the dates that are not present when you do a json query from startDate to endDate
		You don't have to return anything.

		Parameters: stardDate and endDate: strings of the form yyyy-mm-dd
	"""