from algo_lib.algolib import get_data, get_gatillos_compra, get_gatillos_venta, get_acciones, get_trades
from algo_lib.indicators import RSI, SIGMA, CRUCE

df = get_data('BTC-USD', '2015-01-01')

# calculamos las features
rsi = RSI(df)
sigma = SIGMA(df)
cruce = CRUCE(df)
df['rsi'] = rsi
df['sigma'] = sigma
df['cruce'] = cruce
print("Indicators: \n: {}".format(df))

# determinemos los gatillos de compra y de venta
gatillos_compra = get_gatillos_compra(df, ['rsi', 'sigma', 'cruce'])
gatillos_venta = get_gatillos_venta(df, ['rsi', 'cruce'])
print("Gatillos Compra: \n: {}".format(gatillos_compra))
print("Gatillos Venta: \n: {}".format(gatillos_venta))

# get acciones
acciones = get_acciones(gatillos_compra, gatillos_venta)
print("Acciones: \n: {}".format(acciones))

# get trades
trades = get_trades(acciones)
print("Trades: \n: {}".format(trades))


