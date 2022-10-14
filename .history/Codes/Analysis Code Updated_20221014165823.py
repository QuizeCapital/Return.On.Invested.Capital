import sys 
path = "/Users/adamszequi/Desktop/Clones/UniversalModules"
sys.path.append(path)
from ExternalModules import modulesSmartFactor
import pandas as pd
import numpy as np
import json

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
        (key, keyJunior, valueJunior) 
         for elements in openData
         for key, value in elements.items() 
         for keyJunior, valueJunior in value.items() 
        ]

        dataDf = pd.DataFrame(flattenedData, columns = ['Ticker', 'Date', 'ROIC'])
        dataDf['Date'] =  pd.to_datetime(dataDf['Date'], format='%Y-%m-%d')
        dataDf['Date'] = dataDf.Date.dt.year

        groupedData = dataDf.groupby(['Date'])#.apply(lambda a: a[:])

        return [groupedData.get_group(x) for x in groupedData.groups][3:-1]
        
    
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
        
        #flatteing our dictionary so we can easily create a dataframe of our data
        flattenedPriceData = [
        (key, pd.DataFrame(list(value.values()), index=value.keys()))
         for elements in openPriceData
         for key, value in elements.items() 
         #for keyJunior, valueJunior in ast.literal_eval(str(value))
        ]
        # for elements in openPriceData:
        #     for key, value in elements.items():
        #         #print(key, pd.DataFrame(value))
        #         print(key)
        #         #print(ast.literal_eval(value))
        #         value = json.loads(value)
        #         print(pd.DataFrame(list(value.values()), index=value.keys()))
        # priceDataDf = pd.DataFrame(
        #                            flattenedPriceData, 
        #                            columns = ['Ticker', 'Year', 'Annual Log Return']
        #                            )
        
        #return flattenedPriceData
    
        
        
        
        

object  = ROIC(
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/Annual Historical Prices.json',
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/ROIC data.json'   
)    

print(object.cummulativeAnnualGrowthRateQuintiles())       


