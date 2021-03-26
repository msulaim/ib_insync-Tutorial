#Imports
from ib_insync import *
import nest_asyncio

#Establish Connection
nest_asyncio.apply() 
ib = IB()
print(ib.connect())

#Filter account values to get liquidation
print([v for v in ib.accountValues() if v.tag == 'NetLiquidationByCurrency' and v.currency == 'BASE'])

#Disconnect
ib.disconnect()