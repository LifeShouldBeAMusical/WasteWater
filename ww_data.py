import requests, pandas, numpy

def get_data(parameters: dict[str, str]) -> pandas.DataFrame:
	result = requests.get("https://data.cdc.gov/resource/2ew6-ywp6.json", params=parameters)
	
	assert result.status_code == 200
	
	data = pandas.DataFrame(result.json())
	return clean_data(data)

def clean_data(data: pandas.DataFrame) -> pandas.DataFrame:
	data['percentile'] = data['percentile'].astype(float).replace(999.0, numpy.NaN)
	return data

def get_most_recent_data(data: pandas.DataFrame) -> pandas.DataFrame:
	most_recent = data[['wwtp_id', 'date_end']] \
		.groupby('wwtp_id', as_index=False).max()
	most_recent_data = data.join(
		most_recent.set_index(['wwtp_id', 'date_end']),
		on=['wwtp_id', 'date_end'],
		how='inner')
	return most_recent_data
