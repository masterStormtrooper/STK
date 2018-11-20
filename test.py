import Reader, MA

data=Reader.readfile('td.csv')
newdata=MA.find_MA(data,5)
for i in [0,1,2,3,4,5,6,7,8]:
    print(newdata[i])
