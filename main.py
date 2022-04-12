import requests, pandas, datetime, sys, getopt


def main(argv: list[str]):
	(p, v) = get_parsed_arguments(argv)
	
	
	parameters = {}
	if p:
		parameters[p] = v
	# print(parameters)
	
	data = get_data(parameters)
	
	most_recent_data = get_most_recent_data(data)
	
	percent_change_string = "% Change over 15 Days: {percent:.2f}%"
	percent_peak_string = "% of Peak Levels: {percent:.2f}%"

	percent_change = weighted_average(most_recent_data, 'ptc_15d', 'population_served')
	percent_peak = weighted_average(most_recent_data, 'percentile', 'population_served')
	
	print(percent_change_string.format(percent = percent_change))
	print(percent_peak_string.format(percent = percent_peak))

	print("Latest Data:")
	print(most_recent_data[['date_end', 'population_served', 'ptc_15d', 'percentile']])
	

def get_parsed_arguments(argv: list[str]) -> (str, str):
	param = None
	param_value = None
	
	help_string = 'main.py -j <jurisdiction>'
	
	try:
		opts, args = getopt.getopt(argv, "hj:", ["jurisdiction="])
	except getopt.GetoptError:
		print(help_string)
		sys.exit(2)
	for opt, arg in opts:
		# print(opt)
		# print(arg)
		if opt == '-h':
			print("Help")
			print(help_string)
		elif opt in ['-j', '--jurisdiction']:
			param = "reporting_jurisdiction"
			param_value = arg
			print("Jurisdiction: %s" % param_value)
	
	return (param, param_value)

	
def get_data(parameters: dict[str, str]) -> pandas.DataFrame:
	result = requests.get("https://data.cdc.gov/resource/2ew6-ywp6.json", params=parameters)
	
	assert result.status_code == 200
	
	data = pandas.DataFrame(result.json())
	return data

def get_most_recent_data(data: pandas.DataFrame) -> pandas.DataFrame:
	most_recent = data[['wwtp_id', 'date_end']] \
		.groupby('wwtp_id', as_index=False).max()
	most_recent_data = data.join(
		most_recent.set_index(['wwtp_id', 'date_end']),
		on=['wwtp_id', 'date_end'],
		how='inner')
	return most_recent_data



def weighted_average(df: pandas.DataFrame, values: str, weights: str) -> float:
    return sum(df[weights].astype(float) * df[values].astype(float)) / df[weights].astype(float).sum()


if __name__ == "__main__":
	print(sys.argv)
	main(sys.argv[1:])