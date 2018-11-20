"""Read stock prices"""
from datetime import datetime
import csv


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
                result.append([converttodate(i[0]), float(i[1])])
    return result
