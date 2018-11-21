"""Read stock prices"""
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import math


class Stock:
    """Stores the features of stocks"""
    def __init__(self, date, openprice, closingprice, moving_average=None, idx=None):
        self.date = date
        self.op = openprice
        self.cp = closingprice
        self.idx = idx
        if moving_average is None:
            self.ma = {}
        else:
            self.ma = moving_average
        self.bs = 0

    def __repr__(self):
        if self.bs == 0:
            bs = 'N/A'
        elif self.bs == -1:
            bs = 'Sell'
        else:
            bs = 'Buy'
        return "Date:{0}, Opening Price:{1}, Closing Price:{2}, MA: {3}, B/S: {4}"\
            .format(self.date, self.op, self.cp, self.ma, bs)

    def add_bs(self, bs: int):
        """Add a buy/sell to this date. +1 is buy, 0 is do nothing, -1 is sell.
        """
        self.bs = bs

class StockManager:
    """Stores stock prices"""
    def __init__(self, lst):
        self.stocks = lst
        for i in range(len(lst)):
            self.stocks[i].idx = i

    def __getitem__(self, idx):
        return self.stocks[idx]

    def __len__(self):
        return len(self.stocks)

    def __repr__(self):
        for stock in self:
            print(stock)

    def add_stock(self, stock):
        """Add a stock to the manager"""
        # Alan's version
        # loweridx = None
        # for i in range(len(self.stocks)):
        #     the_stock = self.stocks[i]
        #     if the_stock.date < stock.date:
        #         loweridx = i
        # if loweridx is None:
        #     self.stocks.insert(0, stock)
        # else:
        #     self.stocks.insert(loweridx + 1, stock)
        self.stocks.append(stock)


    def findstockbydate(self, dateobj):
        """Find a stock by date"""
        for i in self.stocks:
            the_stock = self.stocks[i]
            if the_stock.date == dateobj:
                return the_stock
        return None

    def plot_price(self, date_range: tuple, plot_bs = False, plot_MA = False):
        """Plot the prices between the date range on a graph. Also plots B/S points. """
        data = self.gethistoryslice(date_range)
        price = []
        for stock in data:
            price.append(stock.cp)
        plt.plot(range(len(data)), price)
        if plot_bs:
            for i in range(len(data.stocks)):
                if data.stocks[i].bs == 1:
                    plt.plot(i, data.stocks[i].cp, 'ro')
                elif data.stocks[i].bs == -1:
                    plt.plot(i, data.stocks[i].cp, 'go')
        if plot_MA:
            MA_dates = []
            for key in data.stocks[0].ma:
                MA_dates.append(key)
            for key in MA_dates:
                xline = list(range(len(data)))
                yline = []
                for i in range(len(data.stocks)):
                    if math.isnan(data.stocks[i].ma[key]):
                        xline.remove(i)
                    else:
                        yline.append(data.stocks[i].ma[key])
                plt.plot(range(len(data)), yline)

    def get_profit(self, use_open = False, ganggan = None):
        """Get the profit/loss percentage based on the buy/sell.
        Buys when self.stock.bs = 1 and sells the when -1.
        Sell all shares before doing anything.

        ganggan: Buy and sell weights. If none, then all buys and sells have weight 1.
        Will implement when the program gets smarter.

        use_open: If True, uses the open price of the next day.
                If false, uses the close price of the previous day.
                Comment: I don't think there should be a big difference.
        """
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
            for stock in self:
                if not first_tr8:
                    if stock.bs == 1:
                        # Should be buying. Means that previous we hold a short position.
                        cr += stock.cp
                        # Buy stock.
                        invested += stock.cp
                        cr += stock.cp
                        trades += 1
                    elif stock.bs == -1:
                        # Should be selling. Means that previous we hold a long position.
                        dr += stock.cp
                        # Short stock.
                        invested += stock.cp
                        dr += stock.cp
                        trades += 1
                else:
                    if stock.bs == 1:
                        # Buy stock.
                        invested += stock.cp
                        cr += stock.cp
                        trades += 1
                        first_tr8 = False
                    elif stock.bs == -1:
                        # Sell stock
                        invested += stock.cp
                        dr += stock.cp
                        trades += 1
                        first_tr8 = False
        return {'trades': trades, 'debit': dr, 'credit': cr,
                'Profit': cr - dr,'Invested': invested, 'Profit Margin': (cr - dr)/invested}

    def gethistoryslice(self, rang=None):
        """Get a slice of history"""
        if rang is None:
            return self
        if isinstance(rang[0], datetime):
            startdate = rang[0]
            enddate = rang[1]
            startidx = self.findstockbydate(startdate).idx
            endidx = self.findstockbydate(enddate).idx
        else:
            assert isinstance(rang[0], int)
            startidx = rang[0]
            endidx = rang[1]
        if endidx == len(self.stocks) - 1:
            return self.__init__(self.stocks[startidx:])
        return StockManager(self.stocks[startidx: endidx + 1])

    def customiter(self, interval, rang=None):
        """Custome iter"""
        historyslice = self.gethistoryslice(rang)
        assert isinstance(interval, int) and interval >= 2
        lst = []
        startidx = interval - 1
        for i in range(startidx, len(historyslice)):
            tmp = [historyslice[i-j] for j in range(interval)]
            tmp.reverse()
            lst.append(tmp)
        return lst


def converttodate(string):
    """Convert string to date"""
    yearlength = len(string.split("/")[-1])
    assert yearlength in [2, 4]
    if yearlength == 2:
        return datetime.strptime(string, "%m/%d/%y")
    else:
        return datetime.strptime(string, "%m/%d/%Y")


def findheaderidx(header, name):
    """Find column idx"""
    for i in range(len(header)):
        if name.upper() in header[i].upper():
            return i
    return None


def readfile(filepth):
    """Read file, return [[date, closing price]...]"""
    result = []
    with open(filepth, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        dateidx = findheaderidx(header, "Date")
        cpidx = findheaderidx(header, "Price")
        opidx = findheaderidx(header, "Open")
        for i in reader:
            if len(i[opidx]) != 0:

                astock = Stock(converttodate(i[dateidx]), float(i[opidx].replace(",", "")),
                               float(i[cpidx].replace(",", "")))
                result.append(astock)
    result.reverse()
    return StockManager(result)
