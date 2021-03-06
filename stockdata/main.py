import pandas as pd
import plotly.graph_objects as go

from stockdata.symbols.getsymbols import Symbols
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

# to download NSE and BSE symbols
def downloadsymbols():
    return Symbols().download()

@SqLite.connector
def getdata(query):
    df = pd.read_sql(query, SqLite.conn)
    df = Utility.reducesize(df)
    return df

def getnsehistprice(symbol):
    if type(symbol) == list:
        symbol = map(lambda x: x.upper().strip(), symbol)
        symbol = "','".join(symbol)
    symbol = symbol.upper().strip()
    df = getdata(f"select * from nsehistprice where symbol in ('{symbol}')")
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

# needs to be corrected
def getweeklynsehistprice(symbol):
    df = getnsehistprice(symbol)
    cols = df.columns
    df = df.reset_index()
    df = df.groupby(['symbol', 'year', 'wknr']).last().reset_index().set_index('date')
    return df[cols]

# needs to be corrected
def getmonthlynsehistprice(symbol):
    df = getnsehistprice(symbol)
    cols = df.columns
    df = df.reset_index()
    df = df.groupby(['symbol', 'year', 'month']).last().reset_index().set_index('date')
    return df[cols]

# needs to be corrected
def getyearlynsehistprice(symbol):
    df = getnsehistprice(symbol)
    cols = df.columns
    df = df.reset_index()
    df = df.groupby(['symbol', 'year']).last().reset_index().set_index('date')
    return df[cols]

def loadtotable(df, tblname):
    df = Utility.reducesize(df)
    SqLite.loadtable(df, tblname)

def searchsymbol(name):
    df = getdata(f"select * from symbols where name like '%{name.upper()}%' or symbol like '%{name.upper()}%'   ")
    return df
