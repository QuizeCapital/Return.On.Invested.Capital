import sys 
path = "/Users/adamszequi/Desktop/Clones/UniversalModules"
sys.path.append(path)
from ExternalModules import modulesSmartFactor
import pandas as pd
import numpy as np
import json
import ast 
import numpy
import pprint
from itertools import groupby
from operator import itemgetter
import statistics
from statistics import mean


class ROIC():
    
    '''
    This functions sets the global variables that will be used
    for our later analysis
    '''
    def __init__(self, annualHistoricalPrices, annualROIC):
        self.annualHistoricalPrices = annualHistoricalPrices
        self.annualROIC = annualROIC
    
    '''
    This function calls the openJson function from the UniversalModules
    class. It takes the return on invested capital data and returns a list
    of dataframe grouped by year.
    '''
    def splitDfYears(self):  
        
        rawData = self.annualROIC
        openData = modulesSmartFactor().openJson(self.annualROIC)
        #flatteingin our dictionary so we can easily
        #create a dataframe of our data
        flattenedData = [
        [key, keyJunior, valueJunior] 
         for elements in openData
         for key, value in elements.items() 
         for keyJunior, valueJunior in value.items() 
        ]
        sorter = sorted(flattenedData, key=itemgetter(0))
        grouper = groupby(sorter, key=itemgetter(0))
        
        return grouper
    '''
    This function takes return of the function 'splitDfYears' which contains our 
    symbol and ROIC data. It then creates a list of lists that contains the
    the quintiles from 0 to 5 and their constituent symbols.
    '''
    def avgROICDf(self):
        
        symbolROIC = self.splitDfYears()

        avgList = []

        for i,j in symbolROIC:

            data = list(map(itemgetter(2), j))
            
            if data:
                dataAvg = [i for i in data if i is not None]
                avgRoic = np.nanmean(dataAvg)
            else:
                avgRoic = None

            avgList.append([i, avgRoic])

        return pd.DataFrame (avgList, columns=['Ticker', 'AvgROIC'])
    
    '''
    This function takes the quintiled ROIC data 
    and returns a lsit of dictionaries containing
    year as key and tickers of five quintiles as values
    '''
    def quintiledROIC(self):
        splitLength = 5

        datadDFList = self.avgROICDf()

        # quinitledDfs = {data.Date.iloc[0]:
        #     data.sort_values(['ROIC'], ascending=[False])
        #     .replace([np.inf, -np.inf], np.nan)
        #     .dropna() 
        #     for data in datadDFList}
        quintiledDfs = datadDFList.sort_values(['AvgROIC'], ascending=[False]).replace([np.inf, -np.inf], np.nan).dropna()

        # return {
        #     key: (np.array_split(value['Ticker'].values, 5))
        #     for key, value in quinitledDfs.items()
        #     }

        split = np.array_split(quintiledDfs, 5)
        return [[num, list(split[num]['Ticker'])]  for num in range(len(split))]
    
    
    
    
    
        
    '''
    This function calculates the cummulative annual growth rate (CAGR).
    The Compound annual growth rates are arranged by quintile, 
    based on the annually run portfolio returns.
    The function takes quintile separated returns data and 
    returns the CAGR for each quintile
    '''
    
    def cummulativeAnnualGrowthRateQuintiles(self):
        
        #lets call our quintiles ROIC function
        tickerQuintiled = self.quintiledROIC()
        
        rawHistoricalPriceData = self.annualHistoricalPrices
        openPriceData = modulesSmartFactor().openJson(rawHistoricalPriceData)
        
        #flattening our dictionary so we can easily create a dataframe of our data
        flattenedPriceData = {
        key:
        pd.DataFrame((json.loads(value).values()), json.loads(value).keys() 
                        )[:-1]
        
        for elements in openPriceData
        for key, value in elements.items() 
        }
        
        
        valueList = []
        keyList = []

        for key,value in flattenedPriceData.items():
            keyList.append(key)
            
            cumprodValuesDf = value.add(1).cumprod()
            
            try:
        #suppose that number2 is a float
                Inverselength = 1/len(cumprodValuesDf)
            except ZeroDivisionError:
                Inverselength = None
  
            latestReturn =  (cumprodValuesDf[-1:]).values
            
            if latestReturn.size>0 and latestReturn[0][0] >= 0:
                latestReturn = latestReturn[0][0]
                # valueList.append(((latestReturn)**Inverselength)-1)              
                valueList.append([key, (np.power(latestReturn, Inverselength))-1])
                #valueList.append(latestReturn[0][0])
            elif latestReturn.size>0 and latestReturn[0][0] < 0:
                latestReturn = abs(latestReturn[0][0])
                # valueList.append(((latestReturn)**Inverselength)-1)              
                valueList.append([key, -((np.power(latestReturn, Inverselength)))-1])
                #valueList.append(latestReturn[0][0])
            else:
                latestReturn = None
                valueList.append([key,latestReturn])
    
        return valueList
    '''
    
    '''
    def crossCheckCAGRROIC (self):
        
        cagr = slef.
        
        
        

object  = ROIC(
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/Annual Historical Prices.json',
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/ROIC data.json'   
)    

pprint.pprint(object.cummulativeAnnualGrowthRateQuintiles())       


