import requests

def getYahooStock(symbol):
    url = "http://download.finance.yahoo.com/d/quotes.csv?s="+ symbol + "&f=sl1d1c1hgvr6r7j1"
    r = requests.get(url)
    rawText = r.text
    rawText = rawText.strip() #get rid of white spac
    print rawText
    list = rawText.split(',')
    data = {}

    data['symbol'] = list[0].replace('"', '')
    data['last'] = list[1]
    data['date'] = list[2].replace('"','')
    data['change'] = list[3]
    data['high'] = list[4]
    data['low'] = list[5]
    data['vol'] = list[6]

    #print "hello"
    return data

getYahooStock("WFC")