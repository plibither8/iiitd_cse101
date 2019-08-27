# Name : Mihir Chaturvedi
# Roll No : 2019061
# Group : A-7

from datetime import datetime, timedelta
from urllib.request import urlopen

BASE_URL = 'https://api.exchangeratesapi.io'

def get_json_string(url):
	""" Returns the json response in 'str' datatype
	"""

	response = urlopen(url).read().decode('utf-8')
	return response

def get_date(date_string):
	""" Returns the date object created from the date string that is supplied
	Parameters: date_string (str): Date string in 'yyyy-mm-dd' format
	Returns: 'date' object
	"""

	year = int(date_string[0:4])
	month = int(date_string[5:7])
	day = int(date_string[8:])
	return datetime(year, month, day)

def getLatestRates():
	""" Returns: a JSON string that is a response to a latest rates query.

	The Json string will have the attributes: rates, base and date (yyyy-mm-dd).
	"""

	url = BASE_URL + '/latest'
	return get_json_string(url)

def changeBase(amount, currency, desiredCurrency, date):
	""" Outputs: a float value f.
	"""

	try:
		datetime.strptime(date, '%Y-%m-%d')
	except ValueError:
		return 'Invalid date format'

	url = BASE_URL + '/' + date
	json_string = get_json_string(url)

	def get_float(code):
		str_start_index = json_string.find(code) + 5
		if str_start_index is 4:
			return False

		str_end_index = json_string.find(',', str_start_index)

		raw_val = json_string[str_start_index:str_end_index]
		if raw_val[len(raw_val) - 1] is '}':
			raw_val = raw_val[:-1]

		return float(raw_val)

	curr_val = get_float(currency)
	des_curr_val = get_float(desiredCurrency)

	if curr_val is False or des_curr_val is False:
		return 'Invalid currency code'

	converted_val = des_curr_val / curr_val * amount
	return converted_val

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
	stardDateStr and endDate: strings of the form yyyy-mm-dd
	currency: a string representing the currency those extremes you have to determine
	"""

	url = BASE_URL + '/history?start_at=' + startDate + '&end_at=' + endDate
	json_string = get_json_string(url)

	rates_start_index = 10
	rates_end_index = -61

	filtered_res = json_string[rates_start_index:rates_end_index] + ','

	start_date = get_date(startDate)
	end_date = get_date(endDate)

	days_till_next_friday = (4 - start_date.weekday()) % 7
	next_friday = start_date + timedelta(days_till_next_friday)

	lowest_val = float('inf')
	highest_val = 0

	a = 1

	while(next_friday <= end_date):
		date_rate_str_start = filtered_res.find(str(next_friday)) + 13
		date_rate_str_end = filtered_res.find('}', date_rate_str_start)
		date_rate_str = filtered_res[date_rate_str_start:date_rate_str_end] + ','

		amount_str_start = date_rate_str.find(currency) + 5
		amount_str_end = date_rate_str.find(',', amount_str_start)
		amount_str = date_rate_str[amount_str_start:amount_str_end]
		amount = float(amount_str)

		if amount < lowest_val:
			lowest_val = amount
			lowest_val_date = str(next_friday)
		if amount > highest_val:
			highest_val = amount
			highest_val_date = str(next_friday)

		next_friday += timedelta(7)

	print(
		currency,
		'was strongest on',
		highest_val_date + '.',
		'1 Euro was equal to',
		str(highest_val),
		currency
	)

	print(
		currency,
		'was weakest on',
		lowest_val_date + '.',
		'1 Euro was equal to',
		str(lowest_val),
		currency
	)

def findMissingDates(startDate, endDate):
	""" Output: the dates that are not present when you do a json query from start_date to endDate
		You don't have to return anything.

		Parameters: stardDate and endDate: strings of the form yyyy-mm-dd
	"""

	url = BASE_URL + '/history?start_at=' + startDate + '&end_at=' + endDate
	json_string = get_json_string(url)

	rates_start_index = 10
	rates_end_index = -61

	filtered_res = json_string[rates_start_index:rates_end_index] + ','

	start_date = get_date(startDate)
	end_date = get_date(endDate)

	print('The following dates were not present:')

	current_date = start_date
	while(current_date <= end_date):
		if filtered_res.find(str(current_date)) is -1:
			print(current_date)
		current_date += timedelta(1)
