# Backtesting Program Ver. 1.1 @ 2024.09.01
# 데이트레이딩 > 변동성 돌파전략
#                              by MIG
# 과거의 데이터를 통한 시뮬레이션이며 미래의 수익을 보장하지 않습니다!!!

import yfinance as yf
import matplotlib.pyplot as plt

init = previous = modified = 5000000 # 초기 투자비
fee = 0.002 # 거래 수수료

ticker = yf.Ticker("000100.KS") # 유한양행
# ticker = yf.Ticker("294090.KS") # Eoflow
# ticker = yf.Ticker("083790.KS") # CG인바이츠
# ticker = yf.Ticker("063160.KS") # 종근당바이오
start_date = "2023-08-01"
# start_date = "2023-02-01"
end_date = "2024-07-31"
data = ticker.history(start=start_date, end=end_date)

# 매수가
data['Target_Price'] = data['Open'] \
    + (data['High'].shift(periods=1) - data['Low'].shift(periods=1)) * 0.5
# 손절가
data['Stop_Loss'] = data['Target_Price'] \
    - (data['High'].shift(periods=1) - data['Low'].shift(periods=1)) * 0.25
data['Mid5'] = data['Close'].rolling(5).mean()
data['Mid10'] = data['Close'].rolling(10).mean()
# 볼린저 밴드
data['Mid20'] = data['Close'].rolling(20).mean()
data['Upper'] = data['Mid20'] + data['Close'].rolling(20).std() * 2
data['Lower'] = data['Mid20'] - data['Close'].rolling(20).std() * 2

data['Meet_Target'] = (data['High'] > data['Target_Price']) \
    & (data['High'] > data['Mid5']) & (data['High'] > data['Mid10'])
    
data['Balance'] = data['Modified'] = 0.0

for ix in data.index:
    if data.loc[ix, 'Mid10'] >= 0:
        if data.loc[ix, 'Meet_Target']:
            # 변동성 돌파 수익
            data.loc[ix, 'Qty'] = int(previous / data.loc[ix, 'Target_Price'])
            data.loc[ix, 'Balance'] = previous + data.loc[ix, 'Qty'] \
                * (data.loc[ix, 'Close'] - data.loc[ix, 'Target_Price']) \
                    - data.loc[ix, 'Qty'] * data.loc[ix, 'Close'] * fee
            # 수정된 변동성 돌파 수익
            if data.loc[ix, 'Low'] < data.loc[ix, 'Stop_Loss']:
                data.loc[ix, 'Modified'] = modified + data.loc[ix, 'Qty'] \
                    * (data.loc[ix, 'Stop_Loss'] - data.loc[ix, 'Target_Price']) \
                        - data.loc[ix, 'Qty'] * data.loc[ix, 'Stop_Loss'] * fee
            else:
                data.loc[ix, 'Modified'] = modified + data.loc[ix, 'Qty'] \
                    * (data.loc[ix, 'Close'] - data.loc[ix, 'Target_Price']) \
                        - data.loc[ix, 'Qty'] * data.loc[ix, 'Close'] * fee
            previous = data.loc[ix, 'Balance']
            modified = data.loc[ix, 'Modified']
        else:
            data.loc[ix, 'Balance'] = previous
            data.loc[ix, 'Modified'] = modified
    else:
        data.loc[ix, 'Balance'] = init
        data.loc[ix, 'Modified'] = init

# 결과 표시
print('변동성 돌파:{:10.2f}%'.format((data.loc[data.index[-1], 'Balance'] - init) / init * 100))
print('손 절 포 함:{:10.2f}%'.format((data.loc[data.index[-1], 'Modified'] - init) / init * 100))

# 12개 표시, x 라벨 간격 조정
ss = []
iv = int(len(data.index)/12)
for i in range(len(data.index)):
    if i % iv == 0:
        ss.append(data.index[i].strftime('%y-%m-%d'))
    else:
        ss.append('')

# 그래프 그리기
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

plt.subplot(211)
plt.title("유한양행 수익")
plt.plot(data['Balance'], 'bs-', label = '변동성 돌파')
plt.plot(data['Modified'], 'rs-', label = '손 절 포 함')
plt.xticks(ticks = data.index, labels = ss)
plt.legend()

plt.subplot(212)
plt.title("유한양행 주가 및 볼린저 밴드")
plt.plot(data['Close'], 'rs-', label = '주가')
plt.plot(data['Mid20'], 'k--', label = '20일 평균')
# plt.plot(data['High'], 'k--', label = '최고가')
# plt.plot(data['Low'], 'k--', label = '최저가')
plt.plot(data['Upper'], 'g--', label = '볼린저 상한')
plt.plot(data['Lower'], 'b--', label = '볼린저 하한선')
plt.xticks(ticks = data.index, labels = ss)
plt.legend()
plt.show()