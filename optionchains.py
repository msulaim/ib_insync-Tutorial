#Imports
from ib_insync import *
import nest_asyncio

#Establish Connection
nest_asyncio.apply() 
ib = IB()
print(ib.connect())

#Create contract
spx = Index('SPX', 'CBOE')
ib.qualifyContracts(spx)

#Request market data, delayed data to avoid problems with permission
ib.reqMarketDataType(4)

#Get the ticker
[ticker] = ib.reqTickers(spx)
#print(ticker)

#Market price
spxValue = ticker.marketPrice()
#print(spxValue)

#Fetch option chains
chains = ib.reqSecDefOptParams(spx.symbol, '', spx.secType, spx.conId)
chains_df = util.df(chains)

#Options trading on SMART
chain = next(c for c in chains if c.tradingClass == 'SPX' and c.exchange == 'SMART')
#print(chain)

#Use the next three-monthly expiries, 
#Use strike prices within +- $20 of the current SPX value, 
#Use strike prices that are a multitude of $5
strikes = [strike for strike in chain.strikes
        if strike % 5 == 0
        and spxValue - 20 < strike < spxValue + 20]
expirations = sorted(exp for exp in chain.expirations)[:3]
rights = ['P', 'C']

contracts = [Option('SPX', expiration, strike, right, 'SMART', tradingClass='SPX')
        for right in rights
        for expiration in expirations
        for strike in strikes]

contracts = ib.qualifyContracts(*contracts)
#print(len(contracts))
#print(contracts[0])

#Get market data for all contracts
tickers = ib.reqTickers(contracts[1])
#print(tickers[0])

#Disconnect
ib.disconnect()