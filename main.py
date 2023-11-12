from algo_lib.algolib import get_data, get_gatillos_compra, get_gatillos_venta
from algo_lib.indicators import RSI, MACD

df = get_data('BTC-USD', '2021-01-01')

# calculamos las features
rsi = RSI(df)
macd = MACD(df)
df['rsi'] = rsi
df['macd'] = macd
print(df.head())

# determinemos los gatillos de compra y de venta
gatillos_compra = get_gatillos_compra(df, ['rsi', 'macd'])
gatillos_venta = get_gatillos_venta(df, ['rsi', 'macd'])


