#Imports
from ib_insync import *
import nest_asyncio
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import pandas as pd
import datetime

#Establish Connection
nest_asyncio.apply() 
ib = IB()
print(ib.connect())


#Create multiple contracts and qualify them
contracts = [Forex(pair) for pair in ('EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'USDCAD', 'AUDUSD')]
ib.qualifyContracts(*contracts)
eurusd = contracts[0]
for contract in contracts:
    ib.reqMktData(contract, '', False, False)

#Create dataframe for storing ticker data    
df = pd.DataFrame(
    index=[c.pair() for c in contracts],
    columns=['bidSize', 'bid', 'ask', 'askSize', 'high', 'low', 'close'])

#0.5 second loop that prints live updated ticker table, it is updated on every ticker change
def onPendingTickers(tickers):
    for t in tickers:
        df.loc[t.contract.pair()] = (
            t.bidSize, t.bid, t.ask, t.askSize, t.high, t.low, t.close)
        clear_output(wait=True)
    display(df)
    print("\n")        

ib.pendingTickersEvent += onPendingTickers
ib.sleep(0.5)
ib.pendingTickersEvent -= onPendingTickers

#Stop live ticker data
for contract in contracts:
    ib.cancelMktData(contract)
    
    
start = ''
end = datetime.datetime.now()
ticks = ib.reqHistoricalTicks(eurusd, start, end, 1000, 'BID_ASK', useRth=False)

print(ticks[-1])


#Disconnect
ib.disconnect()