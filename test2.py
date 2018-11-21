"""Test 2"""
import MA
import Reader
import time
import matplotlib.pyplot as plt
start_time = time.time()


date_range = (10, 100)
MAs = (5, 10)


data = Reader.readfile('td.csv')
new = MA.profit_MA(data, MAs, date_range)
# print(new)
new.plot_price(date_range, True)
plt.show()

print("--- %s seconds ---" % (time.time() - start_time))
