## `Codes`

In this directory, I store two code files of this research project. One for datasets download and the other for
the actual project. Both codes were written in python.

***Data Extraction Code***

The code utilises a class function which consists of child functions that 
call both local and global variables .

The parent class function is called the 'Datasets' function where we set our global variables : 

The only subfunction of our class is called the 'getCleanedDatasets' function.This functions siphons raw datasets from financial modelling prep mainly historical price, eps and free cash flow .Takes global attributes of class and out puts a json file with cleaned datasets for each subfunction containing either fundamental item.

The 'getCleanedEpsData', 'getCleanedFreeCashflowData', 'getCleanedHistoricalPriceData', 'getCleanedFreeCashflowPerShareData', 'Surprise' under the 'getCleanedDatasets' function connects to financial modelling prep's Api
and gets eps, fcfpcs, price, fcf, and earnnings surpise data from various sections as bulk data. Takes original ticker data as parameter and returns returns each tickers data.

***Analysis Code***

The code utilises a class function which consists of child functions that 
call both local and global variables .

The parent class function is called the 'freecashflowpershareByEarnningspershare' function where we set our global variables : 

The first subfunction is called the 'universeAvgReturns' function.This function calculates the average return of our universe of about 3000 equities It takes our log return dataset from our global variables. Returns average of our universe 

The 'epsPctChange' returns the percentage change of earnings per share of our stock universe. It takes the earnings per share data as an undeclared input 

The 'fcfpsPctChange' function calculates the percentage change in free cash flow per share of our universe. It takes a dictionary of symbol, date and free cash flow per share as inputs.It returns a dataframe of symbol, date (most recent date), free cash flow per share of that date, percentage change of free cash flow per share 

The 'FCFPSbyEps' function creates merged 5 quintiles containing intersection of securities based in their eps and free cash flow per share. It takes dataframe of free cash flow and eps as parameter. It returns a 5by5 array of numbers with free cash flow per share as the vertical area and earnings per share as the horizontal area.The values of the array are the mean of returns calculated for each quintile based on the intersection of earnings per share and free cash flow per share for that  quintile

The 'arrayOfFCFPSbyEps' function creates merged 5 quintiles containing intersection of securites based in their eps and free cash flow per share. It takes dataframe of free cash flow and eps as parameter. It returns a dict of number (descending percentage change) as key and list of tickers for that quintile as value
        



