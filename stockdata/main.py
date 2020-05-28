import pandas as pd

from stockdata.symbols.getsymbols import Symbols
from stockdata.historicaldata.loadhistdata import HistData
from stockdata.intraday.downloadintradaydata import IntraDayData
from stockdata.indices.loaddata import Indices
from stockdata.yahoofinance.yf_downloader import YahooFinance
from stockdata.moneycontrol.mc_downloader import MoneyControl
from stockdata.sqlite import SqLite
from stockdata.utils import Utility


@SqLite.connector
def getdata(query):
    df = pd.read_sql(query, SqLite.conn)
    df = Utility.reducesize(df)
    return df

def loadtotable(df, tblname):
    df = Utility.reducesize(df)
    SqLite.loadtable(df, tblname)

def downloadhistdata(startdt='2015-01-01'):
    symbols = Symbols()
    symbols.download()
    del symbols
    i = Indices()
    i.loadindicesdata(startdt)
    del i
    hd = HistData()
    hd.download('NSE', n_symbols=0, loadtotable=True, startdt=startdt)
    hd.download('BSE', n_symbols=0, loadtotable=True, startdt=startdt)
    del hd

def downloadintradaydata(date):
    id = IntraDayData()
    id.download('NSE', date, n_symbols=0)
    id.download('BSE', date, n_symbols=0)
    del id

def downloadprofile():
    mc = MoneyControl()
    mc.downloaddetails(n_symbols=0, loadtotable=True)
    del mc
    yf = YahooFinance()
    yf.downloaddetails('NSE', n_symbols=0, loadtotable=True)
    yf.downloaddetails('BSE', n_symbols=0, loadtotable=True)
    del yf

def downloadnseintradaydata(date, n_symbols=0):
    return IntraDayData().download('NSE', date, n_symbols)

def downloadbseintradaydata(date, n_symbols=0):
    return IntraDayData().download('BSE', date, n_symbols)

def downloadsymbols():
    return Symbols().download()

def downloadindices(startdt='2020-01-01'):
    return Indices().loadindicesdata(startdt)

def downloadnsehistdata(n_symbols=0, loadtotable=True, startdt='2020-01-01'):
    return HistData().download('NSE', n_symbols, loadtotable, startdt)

def downloadbsehistdata(n_symbols=0, loadtotable=True, startdt='2020-01-01'):
    return HistData().download('BSE', n_symbols, loadtotable, startdt)

def downloadnsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('NSE', n_symbols, loadtotable)

def downloadbsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('BSE', n_symbols, loadtotable)

def downloadbsesymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails('BSE', n_symbols, loadtotable)

def downloadnsesymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails('NSE', n_symbols, loadtotable)

def downloadsectorclassify():
    return MoneyControl().getsectorclassif()