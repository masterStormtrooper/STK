import Reader
import MA
import matplotlib.pyplot as plt


data = Reader.readfile('td.csv')
newdata = MA.find_MA(data, 6)
for i in range(6):
    print(newdata[i])
print(newdata[49])
date1 = [44, 45, 46, 47, 48, 49]
date2 = [0, 1, 2, 3, 4, 5]

# MA day 5
temp = 0
for i in date1:
    temp += data[i].cp
print(temp/6)
# MA day 6
temp = 0
for i in date2:
    temp += data[i].cp
print(temp/6)

# price=[]
# for item in data:
#     price.append(item[1])
# MA5 = [0,0,0,0]
# for item in newdata:
#     try:
#         MA5.append(item[2])
#     except:
#         pass
# print(MA5)
# plt.plot(range(len(data)),price)
# plt.plot(range(len(data)),MA5)
# plt.show()
# for i in [0,1,2,3,4,5,6,7,8]:
#     print(newdata[i])
