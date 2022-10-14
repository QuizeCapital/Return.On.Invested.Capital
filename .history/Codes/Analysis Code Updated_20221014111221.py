import sys 
path = "/Users/adamszequi/Desktop/Clones/UniversalModules"
sys.path.append(path)
from ExternalModules import modulesSmartFactor
import pandas as pd
import numpy as np

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
   
        splitGrouped = [groupedData.get_group(x) for x in groupedData.groups][3:-1]

        return splitGrouped
        
    
    '''
    This function takes 
    This function reurns the annual ROIC for each  
    '''
    def quintiledROIC(self):
        
        datadDFList = self.splitDfYears()
        
        quinitledDfs = {data.Date.iloc[0]:
            data.sort_values(['ROIC'], ascending=[False]) 
            for data in datadDFList}
            
        
        return quinitledDfs
    
        
    '''
    This function calculates the cummulative annual growth rate (CAGR).
    The Compound annual growth rates are arranged by quintile, 
    based on the annually run portfolio returns.
    The function takes quintile separated returns data and 
    returns the CAGR for each quintile
    '''
    def cummulativeAnnualGrowthRateQuintiles(self):
        pass
        
        
        

object  = ROIC(
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/Annual Historical Prices.json',
    '/Users/adamszequi/Desktop/Clones/ROIC /Data/ROIC data.json'   
)    

print(object.quintiledROIC())       


