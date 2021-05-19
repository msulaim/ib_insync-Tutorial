#Import ib_insync library
from ib_insync import *
#Import nest_asynchio, allows event loop to be nested
import nest_asyncio
#Import bollinger bands indicator
from btalib import bbands
nest_asyncio.apply()

def instantiate():
    '''
    Purpose: Instantiate an IB object and establish connection
    Return Value: IB object
    '''
    #Intantiate IB class
    ib = IB()
    if ib.isConnected() is False:
        print("\nConnected")
        print(ib.connect())
    
    return ib

def disconnect(ib):
    '''
    Purpose: Disconnect session

    '''
    print("\nDisconnected")
    ib.disconnect()
    return

def getdata():
    
    '''
    Purpose: Creates a contract for a stock, gets historical data related to that stock and applies indicators on it
    '''
    #Create contract using the Stock helper class
    apple_contract = Stock('AAPL', 'SMART', 'USD')
    print("\nStock Details")
    print(ib.qualifyContracts(apple_contract))
    data = ib.reqMktData(apple_contract)
    
   
    
    #Retrieve historical data by using reqHistoricalData to get historical bar data
    historical_data_apple = ib.reqHistoricalData(
                            apple_contract,
                            '',
                            barSizeSetting='15 mins',
                            durationStr='2 D',
                            whatToShow='BID',
                            useRTH=True
                            
                            )

    #The returned object is a BarDataList which supports dataframes and can be converted to one
    apple_df = util.df(historical_data_apple)
    print("\nHistorical Data")
    print(apple_df.head())    
    
    apple_df['20SMA'] = apple_df.close.rolling(20).mean()
    print("\nRolling Mean")
    print(apple_df.close.rolling(20).mean().iloc[-1])
    
    print("\nBollinger Bands")
    print((bbands(apple_df).df).iloc[-1])
    
    return apple_contract, apple_df

def order_status(trade):
    if trade.orderStatus.status == 'Filled':
        fill = trade.fills[-1]
        
        print(f'{fill.time} - {fill.execution.side} {fill.contract.symbol} {fill.execution.shares} @ {fill.execution.avgPrice}')
def createMarketOrder(ib, apple_contract):
    '''
    Purpose: Create a market order which specifies the price to buy the stock at
    '''
    #Create order
    apple_order = MarketOrder('BUY', 1)
    
    #Submit order
    trade = ib.placeOrder(apple_contract, apple_order)
    
    
    return trade

def createBracketOrder(ib, apple_contract):
    '''
    Purpose: Create a bracket order which specifies the price to buy the stock at, the take profit price and the stop loss price
    '''

    
    #Create a bracket order for one share and submit it to the app
    apple_bracket_order = ib.bracketOrder(
        'BUY',
        1,
        limitPrice=123.10,
        takeProfitPrice=125.50,
        stopLossPrice=122.50
    )
    for ord in apple_bracket_order:
        ib.placeOrder(apple_contract, ord)
        
    for ord in apple_bracket_order:
        print (ord)
        print("\n")

def createConditionOrder(ib):
    '''
    Purpose: Create a conditional order, the order gets created for MasterCard when the price of Visa hits a certain price
    '''
    #Create Contract for Visa
    visa_contract = Stock('V', 'SMART', 'USD')
    ib.qualifyContracts(visa_contract)
    
    #Create Price Condition
    price_condition = PriceCondition(
                          price=200,          
                          conId=visa_contract.conId,
                          exch=visa_contract.exchange
                          )
    
    #Create main contract
    ma_contract = Stock('MA', 'SMART', 'USD')
    ib.qualifyContracts(ma_contract)
    
    #Create Order
    visa_ma_order = MarketOrder('BUY', 1)
    
    #Add condition to order
    visa_ma_order.conditions.append(price_condition)
    
    #Place order 
    visa_ma_trade = ib.placeOrder(ma_contract, visa_ma_order)

    return price_condition

def place_order(direction):
	''' place order with IB - exit script if order gets filled '''
	mastercard_order = MarketOrder(direction, 1)
	trade = ib.placeOrder(mastercard_contract, mastercard_order)
	ib.sleep(3)
	if trade.orderStatus.status == 'Filled':
		ib.disconnect()
		quit(0)

if __name__ == "__main__":
    ib = instantiate()
    apple_contract, apple_df = getdata()
    #createBracketOrder(ib, apple_contract)
    #trade = createMarketOrder(ib, apple_contract)
    
    #print(trade.orderStatus.status)
    trade.filledEvent+= order_status
    
    #price_condition = createConditionOrder(ib)
    
    
    disconnect(ib)