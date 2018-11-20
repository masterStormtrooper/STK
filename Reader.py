"""Read stock prices"""
from datetime import datetime
import csv


class StockFeat:
    """Stores the features of stocks"""
    def __init__(self, date, openprice, closingprice, moving_average=None, idx=None):
        self.date = date
        self.op = openprice
        self.cp = closingprice
        self.idx = None
        if moving_average is None:
            self.ma = {}


class StockPrices:
    """Stores stock prices"""
    def __init__(self, lst):
        self.stockhist = lst
        for i in range(len(lst)):
            self.stockhist[i].idx = i

    def findstockbydate(self, dateobj):
        """Find a stock by date"""
        for i in self.stockhist:
            the_stock = self.stockhist[i]
            if the_stock.date == dateobj:
                return the_stock
        return None

    def gethistoryslice(self, rang):
        """Get a slice of history"""
        startdate = rang[0]
        enddate = rang[1]
        startstk = self.findstockbydate(startdate)
        endstk = self.findstockbydate(enddate)
        return self.stockhist[startstk.idx: endstk.idx + 1]

    def customiter(self, interval, rang=None):
        """Custome iter"""
        if rang is None:
            historyslice =



def converttodate(string):
    """Convert string to date"""
    yearlength = len(string.split("/")[-1])
    assert yearlength in [2, 4]
    if yearlength == 2:
        return datetime.strptime(string, "%m/%d/%y")
    else:
        return datetime.strptime(string, "%m/%d/%Y")


def readfile(filepth):
    """Read file, return [[date, closing price]...]"""
    result = []
    with open(filepth, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for i in reader:
            if len(i[1]) != 0:
                result.append([converttodate(i[0]), float(i[1]), float(i[4])])
    result.reverse()
    return result
