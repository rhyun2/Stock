import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

ticker = yf.Ticker("000270.KS") # 기아자동차
# ticker = yf.Ticker("430690.KS") # 한싹
# ticker = yf.Ticker("373220.KS") # LG에너지

start_date = "2024-08-01"
end_date = "2024-08-31"
data = ticker.history(start=start_date, end=end_date)

start_date = "2024-09-02"
end_date = "2024-09-07"
real = ticker.history(start=start_date, end=end_date)

x = list(range(len(data)))
y = data['Close']
fit3 = np.polyfit(x, y, 3)
pf = []

ext = 5
end = list(range(len(data) + ext))
for i in end:
    pf.append(int(fit3[0] * i ** 3 + fit3[1] * i ** 2 + fit3[2] * i + fit3[3]))

ss = []
iv = int(len(x)/6)
for i in range(len(x)):
    if i % iv == 0:
        ss.append(data.index[i].strftime('%m/%d'))
    else:
        ss.append('')
xx = list(range(len(x), len(x)+ext))
yy = pf[len(x):len(x)+ext]
yz = real['Close']

print(yy)
print(yz)

plt.scatter(x, y, c = 'black', s = 50)
plt.scatter(xx, yy, c = 'grey', s = 50)
plt.scatter(xx, yz, c = 'red', s = 50)
plt.plot(end, pf)
plt.xticks(ticks = x, labels = ss, rotation = 'vertical')