#Imports
from ib_insync import *
import nest_asyncio

#Establish Connection
nest_asyncio.apply() 
ib = IB()
print(ib.connect())

#Scanner for top ranked US stock percentage gainers
sub = ScannerSubscription(
    instrument='STK', 
    locationCode='STK.US.MAJOR', 
    scanCode='TOP_PERC_GAIN')

scanData = ib.reqScannerData(sub)

print(f'{len(scanData)} results, first one:')
print(scanData)

#Disconnect
ib.disconnect()