from algo_lib.algolib import get_data, RSI, MACD

df = get_data('BTC-USD', '2021-01-01')

# calculamos las features
rsi = RSI(df)
macd = MACD(df)
df['rsi'] = rsi
df['macd'] = macd
print(df.head())

