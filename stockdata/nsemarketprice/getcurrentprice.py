import sys
import json
import arrow
import requests
import pandas as pd

from requests.adapters import HTTPAdapter

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class CurrentPrice():

    def getjsonstr(self, url):
        headers = { "User-Agent": self.user_agent}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            sys.exit(response)
        json_str = json.loads(response.text)
        return json_str

    def getsymbolscurrentprice(self, json_str):
        plist = []
        data = json_str['data']
        for i in range(len(data)):
            x = {}
            d = data[i]
            x['symbol']         = d['symbol']
            x['open']           = Utility.asfloat(d['open'])
            x['low']            = Utility.asfloat(d['low'])
            x['high']           = Utility.asfloat(d['high'])
            x['ltp']            = Utility.asfloat(d['ltP'])
            x['change']         = Utility.asfloat(d['ptsC'])
            x['changepct']      = Utility.asfloat(d['per'])
            x['volume']         = Utility.asfloat(d['trdVol'])
            x['turnover']       = Utility.asfloat(d['trdVolM'])
            x['yearhigh']       = Utility.asfloat(d['wkhi'])
            x['yearlow']        = Utility.asfloat(d['wklo'])
            x['yearchangepct']  = Utility.asfloat(d['yPC'])
            x['monthchangepct'] = Utility.asfloat(d['mPC'])
            plist.append(x)
        df = pd.DataFrame(plist)
        return df

    def getindicescurrentprice(self, json_str):
        plist = []
        data = json_str['data']
        for i in range(len(data)):
            x = {}
            d = data[i]
            x['time']      = d['timeVal']
            x['index']     = d['indexName']
            x['prevclose'] = Utility.asfloat(d['previousClose'])
            x['open']      = Utility.asfloat(d['open'])
            x['low']       = Utility.asfloat(d['low'])
            x['high']      = Utility.asfloat(d['high'])
            x['ltp']       = Utility.asfloat(d['last'])
            x['yearhigh']  = Utility.asfloat(d['yearHigh'])
            x['yearlow']   = Utility.asfloat(d['yearLow'])
            x['changepct'] = Utility.asfloat(d['percChange'])
            plist.append(x)
        df = pd.DataFrame(plist)
        # df['time'] = pd.to_datetime(json_str['timestamp'])
        # df['openingchange'] = df['open'] - df['prevclose']
        # df['openingtype'] = df['openingchange'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Declines'))
        # df['movement'] = df['pricechange'].apply(lambda x: 'No-Change' if x == 0 else ('Advances' if x > 0 else 'Declines'))
        return df
