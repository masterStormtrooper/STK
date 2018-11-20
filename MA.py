import math
from Reader import *
'''Moving Average analysis'''

def find_MA(data: StockManager, x):
    '''Outputs a new dataframe with the x days MA
     appended to the end'''
    new=StockManager([])
    for i in range(0,x-1):
        the_stock = data[i]
        new_stock = Stock(the_stock.date, the_stock.op,
              the_stock.cp, the_stock.ma)
        new_stock.ma[str(x)] = math.nan
        new.add_stock(new_stock)
    for date in range(x-1,len(data)):
        the_stock = data[date]
        avg=0
        for j in range(x):
            avg+=data[date-j].cp
        avg=avg/x
        new_stock = Stock(the_stock.date, the_stock.op,
                          the_stock.cp, the_stock.ma)
        new.add_stock(new_stock)
        new_stock.ma[str(x)] = avg
    return new

def MAcross_bs(dataframe, MAs: tuple):
    """Given a dataframe, returns floats -1, 0 or 1.
    0 represents do nothing, -1 represents sell,
    1 represents buy."""

def profit_MA(dataframe, MAs: tuple, range: tuple):
    '''
    Outputs the profit of a given period using
    buy/sell tactics when MAs cross.

    Inputs:
    dataframe: The dataframe.
    MAs: Which two MAs to cross.
    range: Date range.
    '''


