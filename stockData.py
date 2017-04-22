import requests
import datetime
from yahoo_finance import Share

def getYahooStock(ticker, date1, date2):
    companyData = Share(ticker)
    dataList = companyData.get_historical(date1, date2)
    endData = dataList[0];
    startData = dataList[len(dataList) - 1];
    print ticker, float(startData['Open']), float(endData['Open'])
    return ticker, float(startData['Open']), float(endData['Open'])

def stockDrop(ticker, date1):
    currentDate = datetime.datetime.now()
    formattedDate = (str(currentDate.year) + '-' + str(currentDate.month) + '-' + str(currentDate.day))
    companyData = Share(ticker)
    dataList = companyData.get_historical(date1, formattedDate);
    originalStock = float(dataList[len(dataList) - 1]['Open']);
    nextLower = 0
    days = -1
    for index, i in enumerate(reversed(dataList)):
        nextLower = i['Open']
        if float(nextLower) < float(originalStock):
            days = len(dataList) - index
            break
    print days, originalStock, nextLower
    return days, originalStock, nextLower

#def stockRange(ticker, date, range):
    #    dateRange = datetime.datetime()

def buyStock(ticker, buyDate, sellDate, amount):
    data = getYahooStock(ticker, buyDate, sellDate)
    print (amount * data[2])/data[1]
    return (amount * data[2])/data[1]

start_date = datetime.datetime(2017, 4, 7, 0)
end_date = datetime.datetime(2017, 4, 14, 0)

d = start_date
delta = datetime.timedelta(hours=1)
print delta
companyData = Share('UAL')
dataList = companyData.get_historical(date1, date2)
while d <= end_date:
    print getYahooStock
    print d.strftime("%Y-%m-%d %H")
    d += delta

stockDrop("BP", '2016-03-29')
getYahooStock("WFC", '2016-03-29', '2017-03-29')
buyStock("WFC", '2016-03-29', '2017-03-29', 1)
