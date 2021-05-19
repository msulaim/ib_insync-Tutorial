#Imports
from ib_insync import *
import nest_asyncio

#Establish Connection
nest_asyncio.apply() 
ib = IB()
print(ib.connect())

#Contract Details
apple_contract = Stock('AAPL')
cds = ib.reqContractDetails(apple_contract)
contracts = [cd.contract for cd in cds]
df_contracts = util.df(contracts)

#Contract which deals on a specifc exchange in a certain currency
apple_smart_usd = Stock('AAPL', 'SMART', 'USD')
assert len(ib.reqContractDetails(apple_smart_usd)) == 1
#print(apple_smart_usd)

#Invalid Stock
#xxx = Stock('XXX', 'SMART', 'USD')
#assert len(ib.reqContractDetails(xxx)) == 0

#Using qualify contracts to fill in information that is sent back when getting the contract details
print('\nBefore Qualifying')
print(apple_smart_usd)
ib.qualifyContracts(apple_smart_usd)
print('\nAfter Qualifying')
print(apple_smart_usd)

#Contracts that match a certain pattern
matches = ib.reqMatchingSymbols('AAPL')
matchContracts = [m.contract for m in matches]
df_match_contracts = util.df(matchContracts)

#Disconnect
ib.disconnect()