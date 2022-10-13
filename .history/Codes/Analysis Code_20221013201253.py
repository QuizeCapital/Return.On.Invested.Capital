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
    class. 
    '''
    def johnDoe(self):  
        
        rawData = self.annualROIC
        openData = modulesSmartFactor().openJson(self.annualROIC)
        
        flattenedData = [
        (key, keyJunior, valueJunior) 
         for elements in openData
         for key, value in elements.items() 
         for keyJunior, valueJunior in value.items() 
        ]
        
        dataDf = pd.DataFrame(flattenedData, columns = ['Ticker', 'Date', 'ROIC'])
        dataDf['Date'] =  pd.to_datetime(dataDf['Date'], format='%Y-%m-%d')

        return dataDf.groupby([dataDf.Date.year])
        #return dataDf
    
    
    '''
    This function reurns the annual ROIC for each  
    '''
    def quintiledROIC(self):
        pass
    
        
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

print(object.johnDoe())       
       
    