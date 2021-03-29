#Imports
from ib_insync import *
import nest_asyncio
from IPython.display import display, clear_output
import pandas as pd


#Establish Connection
nest_asyncio.apply() 
ib = IB()
print(ib.connect())

#Get exchanges that support market depth
l = ib.reqMktDepthExchanges()
#print(l[:5])

#Subscribe to a market depth
contract = Forex('EURUSD')
ib.qualifyContracts(contract)
ticker = ib.reqMktDepth(contract)


#Create dataframe for storing results
df = pd.DataFrame(index=range(5),
        columns='bidSize bidPrice askPrice askSize'.split())

#Event handler
def onTickerUpdate(ticker):
    bids = ticker.domBids
    for i in range(5):
        df.iloc[i, 0] = bids[i].size if i < len(bids) else 0
        df.iloc[i, 1] = bids[i].price if i < len(bids) else 0
    asks = ticker.domAsks
    for i in range(5):
        df.iloc[i, 2] = asks[i].price if i < len(asks) else 0
        df.iloc[i, 3] = asks[i].size if i < len(asks) else 0
    clear_output(wait=True)
    display(df)

ticker.updateEvent += onTickerUpdate

IB.sleep(1);

#Disconnect
ib.disconnect()