# Graph Fitting Model Ver. 1.0 @ 2024.09.14
# 주가예측 > 3차 그래프 모델
#                              by rhyun2
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

ticker = yf.Ticker("000270.KS") # 기아자동차
# ticker = yf.Ticker("430690.KS") # 한싹
# ticker = yf.Ticker("373220.KS") # LG에너지

start_date = "2024-08-01"
end_date = "2024-09-07"
df = ticker.history(start=start_date, end=end_date)

ext = 5 # 예측할 기간
ed = len(df)
md = ed - ext
data = df.iloc[:md, :]
real = df.iloc[md:ed, :]

x = list(range(len(data)))
y = data['Close']
fit3 = np.polyfit(x, y, 3)

# 3차 그래프로 Fitting
pf = []
end = list(range(ed))
for i in end:
    pf.append(int(fit3[0] * i ** 3 + fit3[1] * i ** 2 + fit3[2] * i + fit3[3]))

# 12개 표시, x 라벨 간격 조정
ss = []
iv = int(ed/12)
for i in range(ed):
    if i % iv == 0:
        ss.append(df.index[i].strftime('%m/%d'))
    else:
        ss.append('')
xx = list(range(md, ed))
yy = pf[md:ed]     # 주가 예측
yz = real['Close'] # 실제 주가

print(yy)
print(yz)

# 그래프 설정
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

plt.title("3차 그래프 주가 예측")
plt.scatter(x, y, c = 'black', s = 50)
plt.scatter(xx, yy, c = 'grey', s = 50, label = '주가 예측')
plt.scatter(xx, yz, c = 'red', s = 50, label = '실제 주가')
plt.plot(end, pf)
plt.xticks(ticks = range(ed), labels = ss, rotation = 'vertical')
plt.legend()
plt.show()