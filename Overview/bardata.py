#Imports
from ib_insync import *
import nest_asyncio
from IPython.display import display, clear_output
import matplotlib.pyplot as plt


#Establish Connection
nest_asyncio.apply() 
ib = IB()
print(ib.connect())

# #Earliest date of bar data
# contract = Stock('AAPL', 'SMART', 'USD')
# timestamp = ib.reqHeadTimeStamp(contract, whatToShow='TRADES', useRTH=True)
# #print(timestamp)

# #Hourly data over 60 the last days
# bars = ib.reqHistoricalData(
#         contract,
#         endDateTime='',
#         durationStr='60 D',
#         barSizeSetting='1 hour',
#         whatToShow='TRADES',
#         useRTH=True,
#         formatDate=1)
# df_data = util.df(bars)

# #Plot data as line graph of the closing price
# #df_data.plot(y='close');

# #Plot data as candlestick plot
# #util.barplot(bars[-100:], title=contract.symbol);


# # #Get live updates for historical bars
# # contract = Forex('EURUSD')

# # bars = ib.reqHistoricalData(
# #         contract,
# #         endDateTime='',
# #         durationStr='900 S',
# #         barSizeSetting='10 secs',
# #         whatToShow='MIDPOINT',
# #         useRTH=True,
# #         formatDate=1,
# #         keepUpToDate=True)

# def onBarUpdate(bars, hasNewBar):
#     plt.close()
#     plot = util.barplot(bars)
#     clear_output(wait=True)
#     display(plot)

# # bars.updateEvent += onBarUpdate

# # ib.sleep(10)
# # ib.cancelHistoricalData(bars)

#Event Handler
def onBarLiveUpdate(bars, hasNewBar):
    print(bars[-1])
    print("\n")


contract = Forex('EURUSD')
bars = ib.reqRealTimeBars(contract, 5, 'MIDPOINT', False)
bars.updateEvent += onBarLiveUpdate
ib.sleep(30)
ib.cancelRealTimeBars(bars)

#Disconnect
ib.disconnect()