import requests, pandas, datetime, sys, getopt
from ww_statistic import weighted_average
from ww_data import get_data, get_most_recent_data


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


if __name__ == "__main__":
	print(sys.argv)
	main(sys.argv[1:])
