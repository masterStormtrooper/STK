"""Moving Average analysis"""
import math
from StockModule import *


def get_profit(stockmanager: StockManager, use_open=False, ganggan=None):
    """Get the profit/loss percentage based on the buy/sell.
    Buys when self.stock.bs = 1 and sells the when -1.
    Sell all shares before doing anything.

    ganggan: Buy and sell weights. If none, then all buys and sells have weight 1.
    Will implement when the program gets smarter.

    use_open: If True, uses the open price of the next day.
            If false, uses the close price of the previous day.
            Comment: I don't think there should be a big difference.
    """
    assert len(stockmanager) != 0  # make sure stockmanager is not empty
    trades = 0
    invested = 0
    # Debit and credit
    cr = 0
    dr = 0
    first_tr8 = True
    if use_open:
        # Later
        pass
    else:
        for stock in stockmanager:
            if not first_tr8:
                if stock.bs == "buy":
                    # Should be buying. Means that previous we hold a short position.
                    cr += stock.cp
                    # Buy stock.
                    invested += stock.cp
                    cr += stock.cp
                    trades += 1
                elif stock.bs == "sell":
                    # Should be selling. Means that previous we hold a long position.
                    dr += stock.cp
                    # Short stock.
                    invested += stock.cp
                    dr += stock.cp
                    trades += 1
            else:
                if stock.bs == "buy":
                    # Buy stock.
                    invested += stock.cp
                    cr += stock.cp
                    trades += 1
                    first_tr8 = False
                elif stock.bs == "sell":
                    # Sell stock
                    invested += stock.cp
                    dr += stock.cp
                    trades += 1
                    first_tr8 = False
    return {'trades': trades, 'debit': dr, 'credit': cr,
            'Profit': cr - dr, 'Invested': invested, 'Profit Margin': (cr - dr) / invested}


def find_ma(data: StockManager, ma: tuple):
    """Outputs a new dataframe with the x days MA
     appended to the end
     MAs: a tuple of MAs to find."""
    new = StockManager([])
    # Deep copy
    for i in range(len(data)):
        the_stock = data[i]
        new_stock = Stock(the_stock.date, the_stock.op,
                          the_stock.cp, the_stock.ma)
        new.add_stock(new_stock)
    # Update
    for x in ma:
        for i in range(0, x-1):
            new.stocks[i].ma[str(x)] = math.nan
        for date in range(x-1, len(data)):
            avg = 0
            for j in range(x):
                avg += data[date-j].cp
            avg = avg/x
            new.stocks[date].ma[str(x)] = avg
    return new


def macross_bs(stocks: StockManager, ma: tuple):
    """Given a dataframe, returns floats -1, 0 or 1.
    0 represents do nothing, -1 represents sell,
    1 represents buy."""


def bs_macross(stocks: StockManager, ma: tuple, date_range=()):
    """"
    Outputs the a StockManager with buy/sell tactics updated,
    based on when MAs cross.

    Inputs:
    dataframe: The dataframe.
    MAs: Which two MAs to cross.
    date_range (Tuple): Date range. (STARTS FROM 0)

    Note:
        ma[0] < ma[1]
        0 < date_range[0] < date_range[1] < len(stocks.stocks)
    """
    updated = find_ma(stocks, ma)
    assert ma[0] < ma[1]
    prev_diff = updated[0].ma[str(ma[0])] - updated[0].ma[str(ma[1])]
    for s in range(1, len(updated)):
        diff = updated[s].ma[str(ma[0])] - updated[s].ma[str(ma[1])]
        if not math.isnan(prev_diff) and not math.isnan(prev_diff) and prev_diff*diff < 0:
            if diff > 0:
                updated.stocks[s].add_bs("buy")
            else:
                updated.stocks[s].add_bs("sell")
        prev_diff = diff
    if date_range != ():
        updated = updated.gethistoryslice(date_range)
    return updated
