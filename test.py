import Reader, MA

data=Reader.readfile('td.csv')
print(data)
newdata=MA.find_MA(data,5)
for i in [1,2]:
    print(newdata[i])
