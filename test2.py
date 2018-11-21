from STK import MA, Reader
import time
import matplotlib.pyplot as plt
start_time = time.time()


date_range = (100, 200)
MAs = (5, 10)


data = Reader.readfile('td.csv')
new=MA.bs_MAcross(data, MAs)
# print(new)
# new.plot_price(date_range, True, True)
# plt.show()
print(new.get_profit())

print("--- %s seconds ---" % (time.time() - start_time))