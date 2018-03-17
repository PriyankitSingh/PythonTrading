"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import Q1500US
from quantopian.pipeline.data.sentdex import sentiment
from quantopian.pipeline.data.morningstar import operation_ratios

def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # Rebalance every day, 1 hour after market open.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_open(hours=1),
    )

    # Record tracking variables at the end of each day.
    algo.schedule_function(
        record_vars,
        algo.date_rules.every_day(),
        algo.time_rules.market_close(),
    )

    # Create our dynamic stock selector.
    algo.attach_pipeline(make_pipeline(), 'pipeline')
    
    ##set_commission(commission.PerTrade(cost=0.001))


def make_pipeline():
    # swap this out for testing different alphas
    # tested factors: operation_ratios, revenue_growth, operation_margin, sentiment, 
    #testing_factor = operation_ratios.revenue_growth.latest 
    
    testing_factor1 = operation_ratios.operation_margin.latest
    testing_factor2 = operation_ratios.revenue_growth.latest
    testing_factor3 = sentiment.sentiment_signal.latest
    
    universe = (Q1500US() & 
                testing_factor1.notnull() & 
                testing_factor2.notnull() & 
                testing_factor3.notnull())
    
    testing_factor1 = testing_factor1.rank(mask=universe, method='average')
    testing_factor2 = testing_factor2.rank(mask=universe, method='average')
    testing_factor3 = testing_factor3.rank(mask=universe, method='average')
    
    testing_factor = testing_factor1 + testing_factor2 + testing_factor3
    
    testing_quantiles = testing_factor.quantiles(2)
    
    pipe = Pipeline(columns={'testing_factor':testing_factor, 
                             'shorts':testing_quantiles.eq(0),
                            'longs':testing_quantiles.eq(1)}, screen=universe)
    return pipe


def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    context.output = algo.pipeline_output('pipeline')

    # These are the securities that we are interested in trading each day.
    context.security_list = context.output.index


def rebalance(context, data):
    """
    Execute orders according to our schedule_function() timing.
    This is the actual strategy logic.
    https://www.quantopian.com/posts/how-to-get-an-allocation-writing-an-algorithm-for-the-quantopian-investment-management-team
    Half of your investment money goes towards longing and the other half goes towards shorting
    this keeps beta as low as possible
    TODO: need a stop loss
    """
    long_securities = context.output[context.output['longs']].index # this gives us a list of long securities
    long_weight = 0.5 / len(long_securities)
    
    short_securities = context.output[context.output['shorts']].index # this gives us a list of long securities
    short_weight = - 0.5 / len(short_securities)
    
    for security in long_securities:
        if data.can_trade(security):
            order_target_percent(security, long_weight)
            
    for security in short_securities:
        if data.can_trade(security):
            order_target_percent(security, short_weight)
    
    ## if security is not in long or short, get out of your position
    for security in context.portfolio.positions:
         if data.can_trade(security) and security not in long_securities and security not in short_securities:
                order_target_percent(security, 0)
                

def record_vars(context, data):
    """
    Plot variables at the end of each day.
    Graph your stuff
    """
    long_count = 0
    short_count = 0
    for position in context.portfolio.positions.itervalues():
        if position.amount > 0:
            long_count +=1
        elif position.amount < 0:
            short_count += 1
    record(num_longs = long_count, num_shorts = short_count, leverage = context.account.leverage)


def handle_data(context, data):
    """
    Called every minute.
    """
    pass