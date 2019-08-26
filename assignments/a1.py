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

	URL = BASE_URL + '/' + date
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
	refined_rates_str = json[rates_start_index:rates_end_index] + ','

	number_of_rates = refined_rates_str.count(',')

	lower_bound = 0
	for i in range(number_of_rates):
		loop_start_index = 0
		loop_end_index = refined_rates_str.find(',')

		upper_bound = float('inf')

		for j in range(number_of_rates):
			if loop_end_index < 0:
				break

			rate_str = refined_rates_str[loop_start_index:loop_end_index]
			code = rate_str[1:4]
			amount = float(rate_str[6:])

			if amount < upper_bound and amount > lower_bound:
				upper_bound = amount
				target_code = code
				target_amount = amount

			loop_start_index = loop_end_index + 1
			loop_end_index = refined_rates_str.find(',', loop_start_index)

		lower_bound = upper_bound
		print('1 EUR = ' + str(target_amount) + ' ' + target_code)

def extremeFridays(startDate, endDate, currency):
	""" Output: on which friday was currency the strongest and on which was it the weakest.
		You don't have to return anything.
		
	Parameters: 
	stardDate and endDate: strings of the form yyyy-mm-dd
	currency: a string representing the currency those extremes you have to determine
	"""

	URL = BASE_URL + '/history?start_at=' + startDate + '&end_at=' + endDate
	response = urlopen(URL).read().decode(ENCODING)

	rates_start_index = 10
	rates_end_index = -62

	a = response[rates_start_index:rates_end_index].split('},')
	for b in a:
		print(b)
		print()

# extremeFridays('2019-08-03', '2019-08-07', 0)


def findMissingDates(startDate, endDate):
	""" Output: the dates that are not present when you do a json query from startDate to endDate
		You don't have to return anything.

		Parameters: stardDate and endDate: strings of the form yyyy-mm-dd
	"""