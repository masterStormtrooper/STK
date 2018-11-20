"""Read stock prices"""
from datetime import datetime
import csv


class Stock:
    """Stores the features of stocks"""
    def __init__(self, date, openprice, closingprice, moving_average=None, idx=None):
        self.date = date
        self.op = openprice
        self.cp = closingprice
        self.idx = None
        if moving_average is None:
            self.ma = {}

    def __repr__(self):
        return "Date:{0}, Opening Price:{1}, Closing Price:{2}".format(self.date, self.op, self.cp)


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

    def add(self, stock):
        """Add a stock to the manager"""
        loweridx = None
        for i in range(len(self.stocks)):
            the_stock = self.stocks[i]
            if the_stock.date < stock.date:
                loweridx = i
        if loweridx is None:
            self.stocks.insert(0, stock)
        else:
            self.stocks.insert(loweridx + 1, stock)

    def findstockbydate(self, dateobj):
        """Find a stock by date"""
        for i in self.stocks:
            the_stock = self.stocks[i]
            if the_stock.date == dateobj:
                return the_stock
        return None

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
        return self.__init__(self.stocks[startidx: endidx + 1])

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
    for i in header:
        if name.upper() in i.upper():
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
            if len(i[1]) != 0:
                astock = Stock(converttodate(i[dateidx]), float(i[opidx].replace(",", "")),
                               float(i[cpidx].replace(",", "")))
                result.append(astock)
    result.reverse()
    return StockManager(result)
