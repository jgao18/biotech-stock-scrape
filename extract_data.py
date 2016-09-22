# Example data URL: https://www.google.com/finance/getprices?i=60&p=20d&f=d,o,h,l,c,v&q=ALN
# q - ticker
# x - exchange
# i - interval (seconds)
# p - period (days)
# f - fields (date, open, close, high, low, volume)

# usage: python extract_data.py period ticker1 ticker2 ticker3...

import os
import sys
import urllib
import datetime

interval = 60 # seconds
period = sys.argv[1]

# Extracting data from Google Finance API for each ticker
for ticker in sys.argv[2:]:
    # Collecting normal hours and extended hours data
    normalURL = "https://www.google.com/finance/getprices?i=" + str(interval) + "&p=" + period + "d&f=d,o,h,l,c,v&q=" + ticker
    extendedURL = "https://www.google.com/finance/getprices?i=" + str(interval) + "&sessions=ext_hours&p=" + period + "d&f=d,o,h,l,c,v&q=" + ticker

    normalStream = urllib.urlopen(normalURL)
    normalDataString = normalStream.read()

    extendedStream = urllib.urlopen(extendedURL)
    extendedDataString = extendedStream.read()

    normalDataList = normalDataString.splitlines();
    extendedDataList = extendedDataString.splitlines();

    combinedDataList = normalDataList + extendedDataList[8:]

    # Collecting each tick's data
    tickData = []
    for tick in combinedDataList[7:]:
        tickList = tick.split(',')
        if tick[0] == 'a':
            startTimeUnix = int(tickList[0][1:])
            tickTime = datetime.datetime.fromtimestamp(startTimeUnix).strftime('%m-%d-%Y %H:%M:%S')
        else:
            tickTimeUnix = startTimeUnix + 60*int(tickList[0])
            tickTime = datetime.datetime.fromtimestamp(tickTimeUnix).strftime('%m-%d-%Y %H:%M:%S')

        tickClose = float(tickList[1])
        tickHigh = float(tickList[2])
        tickLow = float(tickList[3])
        tickOpen = float(tickList[4])
        tickVolume = float(tickList[5])

        tickValues = [tickTime, tickVolume, tickOpen, tickHigh, tickLow, tickClose]

        tickData.append(tickValues)

    # Sort data by date
    tickData.sort(key=lambda x: x[0])

    # Locate proper directory to save data dump
    scriptDirectory = os.path.dirname(__file__)

    if not os.path.isdir(ticker): # create ticker directory if one doesn't exist
        os.mkdir(ticker)
                 
    localPath = ticker + "\\" + ticker + "_data.csv"
    filePath = os.path.join(scriptDirectory, localPath)

    # Appened data to data file
    with open(filePath, "a") as dataFile:
        for tick in tickData:
            dataFile.write(tick[0] + "," + str(tick[1]) + "," +str(tick[2]) + "," +str(tick[3]) + "," +str(tick[4]) + "," +str(tick[5]) + "\n")
    dataFile.close()

    # Remove duplicates
    timesSeen = []
    uniqueLines = []
    with open(filePath, "r") as dataFile:
        for line in dataFile:
            timestamp = line.split(',')[0]
            if timestamp not in timesSeen:
                timesSeen.append(timestamp)
                uniqueLines.append(line)
    dataFile.close()

    uniqueLines.sort() # resort before rewriting
    with open(filePath, "w") as dataFile:
        for line in uniqueLines:
            dataFile.write(line)
    dataFile.close()

    # Record extraction in history file
    extractHistoryFile = os.path.join(scriptDirectory, "extract_history.txt")
    with open(extractHistoryFile, "a") as historyFile:
        date = datetime.datetime.today().strftime("%m/%d/%Y")
        historyFile.write(date + " - " + ticker + ", " + period + "d" + "\n")
    historyFile.close()
