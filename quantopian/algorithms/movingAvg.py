'''
This script is meant to be run on quantopian. It won't compile with normal python.
'''

'''
Method called in the beginning of runtime
'''
def initialize(context):
    print ("Initializing algorithm")
    context.aapl = sid(24) # get the apple stock
    schedule_function(movingAvgCrossover, 
                      date_rules.every_day(), 
                      time_rules.market_open(hours=1))
  
def movingAvgCrossover(context, data):
    hist = data.history(context.aapl, 'price', 50, '1d')
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()
    
    ## check if we're doubling up on orders this is to prevent going over our leverage
    openOrders = get_open_orders()
    
    
    if sma_20 > sma_50:
        if context.aapl not in openOrders:
            order_target_percent(context.aapl, 1.0)
    elif sma_20 < sma_50:
        if context.aapl not in openOrders:
            order_target_percent(context.aapl, -1.0)
    record(leverage = context.account.leverage)