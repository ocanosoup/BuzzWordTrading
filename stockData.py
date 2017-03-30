import requests
from yahoo_finance import Share

def getYahooStock(ticker, date1, date2):
    companyData = Share(ticker)
    dataList = companyData.get_historical(date1, date2)
    startData = dataList[0];
    endData = dataList[1];
    return ticker, float(startData['Open']), float(endData['Open'])

#getYahooStock("WFC", '2016-03-29', '2017-03-29')