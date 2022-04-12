import pandas

def weighted_average(df: pandas.DataFrame, values: str, weights: str) -> float:
    return sum(df[weights].astype(float) * df[values].astype(float)) / df[weights].astype(float).sum()
