import pandas

def weighted_average(df: pandas.DataFrame, values: str, weights: str) -> float:
	kosher_idx = ~df[values].isna()
	return sum(df.loc[kosher_idx, weights].astype(float) * df.loc[kosher_idx, values].astype(float)) / df.loc[kosher_idx, weights].astype(float).sum()
