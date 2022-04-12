import requests
import pandas
import datetime


def main():
	parameters = {"reporting_jurisdiction": "Chicago"}

	result = requests.get("https://data.cdc.gov/resource/2ew6-ywp6.json", params=parameters)
	
	assert result.status_code == 200

	data = pandas.DataFrame(result.json())

	most_recent = data[['wwtp_id', 'date_end']].groupby('wwtp_id', as_index=False).max()

	most_recent_data = data.join(most_recent.set_index(['wwtp_id', 'date_end']), on=['wwtp_id', 'date_end'], how='inner')
	
	
	print(most_recent_data[['date_end', 'population_served', 'ptc_15d', 'percentile']])
	

	print(weighted_average(most_recent_data, 'ptc_15d', 'population_served'))
	print(weighted_average(most_recent_data, 'percentile', 'population_served'))

def weighted_average(df: pandas.DataFrame, values: str, weights: str) -> float:
    return sum(df[weights].astype(float) * df[values].astype(float)) / df[weights].astype(float).sum()


if __name__ == "__main__":
	main()