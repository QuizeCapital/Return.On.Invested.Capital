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
        res = {i: list(map(itemgetter(2), j)) for i, j in grouper}
        #pprint.pprint(res)
        avgList = []
        
        for i,j in grouper:
            print(i)
            data = (list(map(itemgetter(2), j)))
            if len(data) > 0:
                dataAvg = [i for i in data if i is not None]
                #print(data)
                avgRoic = np.nanmean(dataAvg)
            else:
                avgRoic = None
            
            

            avgList.append([i, avgRoic])
        #mean(d for d in data[0] if d is not None)

        #res = {i: (mean(list(map(itemgetter(2), j))) if len(list(map(itemgetter(2), j))) != None else 0) for i, j in grouper}



        dataDf = pd.DataFrame(flattenedData, columns = ['Ticker', 'Date', 'ROIC'])
        dataDf['Date'] =  pd.to_datetime(dataDf['Date'], format='%Y-%m-%d')
        dataDf['Date'] = dataDf.Date.dt.year

        groupedData = dataDf.groupby(['Date'])#.apply(lambda a: a[:])

        #return [groupedData.get_group(x) for x in groupedData.groups][:-1]
        return avgList
    
    '''
    This function takes the quintiled ROIC data 
    and returns a lsit of dictionaries containing
    year as key and tickers of five quintiles as values
    '''
    def quintiledROIC(self):
        
        datadDFList = self.splitDfYears()

        quinitledDfs = {data.Date.iloc[0]:
            data.sort_values(['ROIC'], ascending=[False])
            .replace([np.inf, -np.inf], np.nan)
            .dropna() 
            for data in datadDFList}

        return {
            key: (np.array_split(value['Ticker'].values, 5))
            for key, value in quinitledDfs.items()
            }
    
        
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
    
        #return valueList
    
    
        
        

object  = ROIC(
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/Annual Historical Prices.json',
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/ROIC data.json'   
)    

print(object.splitDfYears())       


