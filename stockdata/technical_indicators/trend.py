import pandas as pd
import ta


from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class TrendIndicators():

    def MA(self, df, n):
        name=f'ma{n}d'
        df[name] = df.groupby('symbol').close.transform(lambda x: x.rolling(n).mean().fillna(0).round(2))
        return df

    def EMA(self, df, n):
        name=f'ema{n}d'
        df[name] = df.groupby('symbol').close.transform(lambda x: x.ewm(span=n, adjust=False).mean().fillna(0).round(2))
        return df
