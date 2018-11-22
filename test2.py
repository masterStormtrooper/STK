"""Test"""
import MovingAverageStrategy as Ma
import StockModule
import time
import matplotlib.pyplot as plt
start_time = time.time()


date_range = (100, 200)
MAs = (5, 10)


data = StockModule.readfile('td.csv')
new = Ma.bs_macross(data, MAs)
# print(new)
# new.plot_price(date_range, True, True)
# plt.show()
print(Ma.get_profit(new))

print("--- %s seconds ---" % (time.time() - start_time))
