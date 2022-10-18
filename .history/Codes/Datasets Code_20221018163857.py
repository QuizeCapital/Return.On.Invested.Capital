import sys 
path = "/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Universal Models"
sys.path.append(path)
from ExternalModules import modulesSmartFactor
from urllib.request import urlopen
import certifi
import json
from dateutil.parser import isoparse
from operator import itemgetter
import pandas as pd
import numpy as np
from scipy.stats import gmean

'''
Datasets codes for this SubProject
'''
class Datasets:
    '''
    setting our variables
    '''
    def __init__(self, ROIC, tickerData, logReturnsData, annuallogReturnsData, annuallogReturnsSandPData, annualMarketCapitalization, quarterlyLogReturnsData, annualQuarterlylogReturnsSandPData):
        #this is where we dump our ROIC data
        self.ROIC = ROIC
        #this is where we get our tickers
        self.tickerData = tickerData
        #this is where we store or logarithmic returns data
        self.logReturnsData = logReturnsData
        #this is where we store our annual logarithmic returns data
        self.annuallogReturnsData = annuallogReturnsData
        #this is where we store our annual logarithmic returns data
        self.annuallogReturnsSandPData = annuallogReturnsSandPData
        #this is where we store our annual logarithmic returns data for all tickers
        self.annualMarketCapitalization = annualMarketCapitalization
        #this is where we store or logarithmic returns data
        self.quarterlyLogReturnsData = quarterlyLogReturnsData
        #this is where we store our quarterly annual logarithmic returns data
        self.annualQuarterlylogReturnsSandPData = annualQuarterlylogReturnsSandPData
    '''
    This functions siphons raw  return on capital datasets from financial modelling prep
    
    Takes global attributes of class and out puts a json file with cleaned datasets for each 
    subfunction containing either fundamnetal item
    
    
    '''   
    def getCleanedDatasets(self):
            #empty list  to append the  diicts
            # #of symbol, date and revenue per share
            #for loop data that we siphon into
        dataDictList = []
        '''
        This function connects to financial modelling prep's Api
        and gets eps data from the income statement section 
        as bulk data 
        Takes original ticker data as parameter and returns 
        returns each tickers data with limit of 7 years
        '''

        def getCleanedROICData(self):  # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                
                #Api connection with 500 limit as we need data for all years 
                #and feeding in the ticker name
                url = f'https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?limit=500&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")

                if  bulkData := json.loads(data):
                    #bulk income statement data 
                    dict = bulkData
            
                    for dictionaryValue in dict:
                            dictInfo =  {dictionaryValue.get('symbol'): {dictionaryValue.get('date'): dictionaryValue.get('roic')}}
                            print(count)
                            print(dictInfo)
                            dataDictList.append(dictInfo)
                            

            return modulesSmartFactor().dumpJson(self.ROIC, dataDictList)
            
        def getCleanedHistoricalPriceData(self):
            #initialise a list with dict
            #of annualised logreturns
            dictReturns = []
            # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                #Api connection wfor historical data for 2021
                url = f'https://financialmodelingprep.com//api/v3/historical-price-full/{ticker}?serietype=line&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")
                if  bulkData := json.loads(data):
                    #bulk price data
                    dict = bulkData
                    #get adjusted close data from 
                    #historical data 
                    #priceInfoBulk = list((map(itemgetter('adjClose'),dict.get('historical', {}))))
                    priceInfoBulk = list((map(itemgetter('close', 'date'),dict.get('historical', {}))))
                    #get dymbol attached to adjusted close
                    symbol = (dict.get('symbol', {}))
                    priceDf = pd.DataFrame(priceInfoBulk, columns = ['price', 'date']).iloc[::-1]
                    priceDf['date'] = pd.to_datetime(priceDf['date'], errors='coerce').dt.year
                    PRINT priceDf
                    priceDf['pct_ch'] = (
                        priceDf.groupby(priceDf.date)['price']
                                #.apply(((pd.Series.pct_change) + 1)).sum()
                                  .apply(
                                      [lambda x: (np.log(x) - np.log(x.shift(1)))]
                                      )            
                        )
                    print(priceDf)
                    groupedPrice = (priceDf.groupby('date')['pct_ch'].sum()).to_json()

                    groupedPriceData = {symbol: groupedPrice}
                     
                    dictReturns.append(groupedPriceData)
                    
                    print(count)
                    print(groupedPriceData)

             #dump data into returns json file by 
             #calling dumpjson attribute in modules file       
            return modulesSmartFactor().dumpJson(self.annuallogReturnsData , dictReturns)  
        
        def getCleanedSandPHistoricalData(self):  # sourcery skip: avoid-builtin-shadow
            try:
    # For Python 3.0 and later
                from urllib.request import urlopen
            except ImportError:
                from urllib2 import urlopen

            def get_jsonparsed_data(url):

                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")
                return json.loads(data)

            url = ("https://financialmodelingprep.com/api/v3/historical-price-full/index/%5EGSPC?&from=1800-03-10&to=2022-09-28&apikey=764a0c82850f17c8235116b78792d7e1")
            dictSp = get_jsonparsed_data(url)
            dataDictList.append(dictSp)        
      
            return modulesSmartFactor().dumpJson(self.annuallogReturnsSandPData, dataDictList)
        
        def getCleanedAnnualMarketCapData(self):  # sourcery skip: avoid-builtin-shadow
            
            dictMarkCap = []
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                
                #Api connection with 500 limit as we need data for all years 
                #and feeding in the ticker name
                url = f'https://financialmodelingprep.com/api/v3/historical-market-capitalization/{ticker}?&from=1800-03-10&to=2022-09-28&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")

                if  bulkData := json.loads(data):
                    #bulk income statement data 
                    dictData = bulkData
            
                    data = dictData
                    dataDf = pd.DataFrame(data)

                    dataDf['date'] = pd.to_datetime(dataDf['date'], errors='coerce').dt.year
                    groupedDataSeries = dataDf.groupby('date')['marketCap'].mean()
                    groupedDataDf= pd.DataFrame({'Year':groupedDataSeries.index, 'Arithmetic Mean : Market Cap':groupedDataSeries.values})

                    groupedDataSeriesGmean= (dataDf.groupby('date')['marketCap'].apply(gmean, axis=0))
                    groupedDataDfGmean= pd.DataFrame({'Year':groupedDataSeriesGmean.index, 'Geometric Mean : Market Cap':groupedDataSeriesGmean.values})
                    #We use geometric mean as Mornig str uses
                    #https://www.morningstar.com/invglossary/average_market_capitalization.aspx
                    dfArithmeticGeometricMean = (pd.concat([groupedDataDfGmean, groupedDataDf], axis='columns').T.drop_duplicates().T).to_dict()
                    print(count, ticker, (pd.concat([groupedDataDfGmean, groupedDataDf], axis='columns').T.drop_duplicates().T).head())
                    dictMarkCap.append([ticker,dfArithmeticGeometricMean])
                    
            return modulesSmartFactor().dumpJson(self.annualMarketCapitalization, dictMarkCap)    
        
        def getCleanedQuarterlyHistoricalPriceData(self):
            #initialise a list with dict
            #of annualised logreturns
            dictQuartReturns = []
            # sourcery skip: avoid-builtin-shadow
            for count, ticker in enumerate(modulesSmartFactor().openCsv(self.tickerData)['Ticker'], start=1):
                #Api connection wfor historical data for 2021
                url = f'https://financialmodelingprep.com//api/v3/historical-price-full/{ticker}?serietype=line&apikey=764a0c82850f17c8235116b78792d7e1'
                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")
                if  bulkData := json.loads(data):
                    #bulk price data
                    dict = bulkData
                    #get adjusted close data from 
                    #historical data 
                    #priceInfoBulk = list((map(itemgetter('adjClose'),dict.get('historical', {}))))
                    priceInfoBulk = list((map(itemgetter('close', 'date'),dict.get('historical', {}))))
                    #get dymbol attached to adjusted close
                    symbol = (dict.get('symbol', {}))
                    priceDf = pd.DataFrame(priceInfoBulk, columns = ['price', 'date']).iloc[::-1]
                    
                    #priceDf.date = pd.to_datetime(priceDf.date)
                    
                    priceDf['quarter'] = pd.PeriodIndex(priceDf.date, freq='Q')
                    # priceDf['date'] = pd.to_datetime(priceDf['date'], errors='coerce').dt.year
              
                    priceDf['pct_ch'] = (
                            priceDf.groupby(priceDf.quarter)['price']
                                #  .apply(((pd.Series.pct_change) + 1)).sum())
                                  .apply(
                                      lambda x: (np.log(x) - np.log(x.shift(1)))
                                      )            
                        )
                    
                    groupedPrice = (priceDf.groupby('quarter')['pct_ch'].sum()).to_json()

                    groupedPriceData = {symbol: groupedPrice}
                     
                    dictQuartReturns.append(groupedPriceData)
                    
                    print(count)
                    # print(groupedPriceData)
                    # print(groupedPriceData)

             #dump data into returns json file by 
             #calling dumpjson attribute in modules file       
            return modulesSmartFactor().dumpJson(self.quarterlyLogReturnsData ,dictQuartReturns)      
        
        def getCleanedSandPQuarterlyHistoricalData(self):  
            
            QuarterlylogReturnsSandPlist = []
            # sourcery skip: avoid-builtin-shadow
            try:
    # For Python 3.0 and later
                from urllib.request import urlopen
            except ImportError:
                from urllib2 import urlopen

            def get_jsonparsed_data(url):

                response = urlopen(url, cafile=certifi.where())
                data = response.read().decode("utf-8")
                return json.loads(data)

            url = ("https://financialmodelingprep.com/api/v3/historical-price-full/index/%5EGSPC?&from=1800-03-10&to=2022-09-28&apikey=764a0c82850f17c8235116b78792d7e1")
            dictSp = get_jsonparsed_data(url)
            QuarterlylogReturnsSandPlist.append(dictSp)        
      
            return modulesSmartFactor().dumpJson(self.annualQuarterlylogReturnsSandPData, dataDictList)
        
        return getCleanedHistoricalPriceData(self)
        

outPut = Datasets(
    "/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/ROIC/ROIC data.json"
    ,"/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Master Dataset File/marketCapDataCleaned.csv"
    ,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/ROIC/Historical Prices.json'
    ,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/ROIC/Annual Historical Prices.json'
    ,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/ROIC (Single Factor Strategy)/Data/Annual S&P Historical Prices.json'
    ,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/ROIC (Single Factor Strategy)/Data/Annual Market Capitalization.json'
    ,'/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/ROIC (Single Factor Strategy)/Data/Quarterly Log returns.json'
    ,'/Users/adamszequi/Desktop/Clones/ROIC /Data/Annual S&P Data.json'
)    
(outPut.getCleanedDatasets())
            
        
# print((modulesSmartFactor().openCsv("/Users/adamszequi/SmartFactor/Smart-Factor-Research-Files-5/Master Dataset File/marketCapDataCleaned.csv")).columns)