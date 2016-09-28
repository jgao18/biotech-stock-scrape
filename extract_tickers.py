# Extracts ticker from biopharmcatalyst website

# usage: python extract_data.py period ticker1 ticker2 ticker3...

import urllib
import urllib2
import re
import os

# Get page source of bio website
webResponse = urllib2.urlopen("https://biopharmcatalyst.com/calendars/fda-calendar")
webSource = webResponse.read()

sourceSplit = webSource.split("<")

# Compile all tickers and their catalysts into a list
tickerList = []
lineCounter = 0
for line in sourceSplit:
    if "/company/" in line:
        regTicker = re.search('/company/(.*)" class="ticker">', line)
        ticker = regTicker.group(1)
        # For some reason, a couple tickers have "-1" added at the end
        if "-1" in ticker:
            ticker = ticker[:-2]
        tickerList.append(ticker.upper())
    if 'catalyst-note">' in line:
        regCatalyst = re.search('"catalyst-note">(.*)', line)
        catalystLine = regCatalyst.groups()
        catalyst = ''.join(catalystLine)
        # If the catalyst is empty, then the page source text is messed up, so additional parsing is needed
        if catalyst == "":
            scrambledCatalyst = sourceSplit[lineCounter + 1] + sourceSplit[lineCounter + 2]
            filingTypeReg = re.search('"caps">(.*)/span>', scrambledCatalyst)
            filingType = filingTypeReg.group(1)
            unscrambledCatalystReg = re.search('/span>(.*)', scrambledCatalyst)
            unscrambledCatalyst = unscrambledCatalystReg.group(1)
            combinedCatalyst = filingType + unscrambledCatalyst
            combinedCatalyst = combinedCatalyst.replace("&nbsp;", " ")
            tickerList[-1] = tickerList[-1] + ": " + combinedCatalyst
        else:
            catalyst = catalyst.replace("&nbsp;", " ")
            tickerList[-1] = tickerList[-1] + ": " + catalyst      
    lineCounter += 1

tickerList = sorted(tickerList)

# Writes tickers/catalysts to file

with open("bio_tickers.txt", "w") as dataFile:
    for ticker in tickerList:
        dataFile.write(ticker + "\n")
dataFile.close()



# Runs extract_data.py on each ticker
'''
tickersOnlyList = []
for ticker in tickerList:
    tickerOnly = ticker.rsplit(':', 1)[0]
    tickersOnlyList.append(tickerOnly)

tickersOnlyList = set(tickersOnlyList)

for ticker in tickersOnlyList:
    os.system("extract_data.py 20 " + ticker)
'''
