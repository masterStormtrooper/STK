'''Moving Average analysis'''

def find_MA(dataframe, x):
    '''Outputs a new dataframe with the x days MA
     appended to the end'''
    new=[]
    for date in range(0,x):
        new.append(dataframe[date])
    for date in range(x,len(dataframe)):
        avg=0
        for j in range(x):
            avg+=dataframe[date-j][2]
        avg=avg/x
        new.append(dataframe[date]+[avg])
    return new

def profit_MA(dataframe, range:tuple):
    '''Inputs the dataframe with the MA.
    '''