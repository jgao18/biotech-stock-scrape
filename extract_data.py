# Example data URL: https://www.google.com/finance/getprices?i=60&p=20d&f=d,o,h,l,c,v&q=ALN
# q - ticker
# x - exchange
# i - interval (seconds)
# p - period (days)
# f - fields (date, open, close, high, low, volume)
import urllib
import datetime

# Extracting data from Google Finance API
ticker = "AAPL"
interval = "60" # seconds
period = "20" # days

# Collecting normal hours and extended hours data
normalURL = "https://www.google.com/finance/getprices?i=" + interval + "&p=" + period + "d&f=d,o,h,l,c,v&q=" + ticker
extendedURL = "https://www.google.com/finance/getprices?i=" + interval + "&sessions=ext_hours&p=" + period + "d&f=d,o,h,l,c,v&q=" + ticker

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

    #tickValues = [tickTime, tickClose, tickHigh, tickLow, tickOpen, tickVolume]
    tickValues = [tickTime, tickLow, tickOpen, tickClose, tickHigh]

    tickData.append(tickValues)

# Sort data by date
tickData.sort(key=lambda x: x[0])

for tick in tickData:
    print tick
