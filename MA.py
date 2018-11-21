import math
from Reader import *
'''Moving Average analysis'''

def find_MA(data: StockManager, MAs: tuple):
    '''Outputs a new dataframe with the x days MA
     appended to the end
     MAs: a tuple of MAs to find.'''
    new = StockManager([])
    # Deep copy
    for i in range(len(data)):
        the_stock = data[i]
        new_stock = Stock(the_stock.date, the_stock.op,
                          the_stock.cp, the_stock.ma)
        new.add_stock(new_stock)
    # Update
    for x in MAs:
        for i in range(0,x-1):
            new.stocks[i].ma[str(x)] = math.nan
        for date in range(x-1,len(data)):
            avg=0
            for j in range(x):
                avg+=data[date-j].cp
            avg=avg/x
            new.stocks[date].ma[str(x)] = avg
    return new

def MAcross_bs(stocks: StockManager, MAs: tuple):
    """Given a dataframe, returns floats -1, 0 or 1.
    0 represents do nothing, -1 represents sell,
    1 represents buy."""



def bs_MAcross(stocks: StockManager, MAs: tuple, date_range = ()):
    '''
    Outputs the a StockManager with buy/sell tactics updated,
    based on when MAs cross.

    Inputs:
    dataframe: The dataframe.
    MAs: Which two MAs to cross.
    date_range (Tuple): Date range. (STARTS FROM 0)

    Note:
        MAs[0] < MAs[1]
        0 < date_range[0] < date_range[1] < len(stocks.stocks)
    '''
    updated = find_MA(stocks, MAs)

    if math.isnan(updated[0].ma[str(MAs[0])] - updated[0].ma[str(MAs[1])]):
        diff = [math.nan]
    else:
        diff=[updated[0].ma[str(MAs[0])] - updated[0].ma[str(MAs[1])] > 0]
    for s in range(1, len(updated)):
        diff.append(updated[s].ma[str(MAs[0])] - updated[s].ma[str(MAs[1])] > 0)
        if math.isnan(diff[s]) or math.isnan(diff[s - 1]):
            pass
        elif diff[s] != diff[s-1]:
            if diff[s] is True:
                updated.stocks[s].add_bs(1)
            else:
                updated.stocks[s].add_bs(-1)
    if date_range != ():
        updated = updated.gethistoryslice(date_range)
    return updated