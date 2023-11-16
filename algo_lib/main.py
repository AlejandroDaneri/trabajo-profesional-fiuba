from algolib import *
from indicators import *
from indicators.rsi import RSI
from indicators.sigma import Sigma
from indicators.crossing import Crossing

df = get_data('BTC-USD', '2015-01-01')

# calculamos las features
rsi = RSI()
sigma = Sigma()
cruce = Crossing()
df['rsi'] = rsi.calculate(df)
df['sigma'] = sigma.calculate(df)
df['cruce'] = cruce.calculate(df)
print("Indicators: \n: {}".format(df))

# determinemos los gatillos de compra y de venta
gatillos_compra = get_buy_signals(df, [rsi, sigma, cruce])
gatillos_venta = get_buy_signals(df, [rsi, cruce])
print("Gatillos Compra: \n: {}".format(gatillos_compra))
print("Gatillos Venta: \n: {}".format(gatillos_venta))

# get acciones
acciones = get_actions(gatillos_compra, gatillos_venta)
print("Acciones: \n: {}".format(acciones))

# get trades
trades = get_trades(acciones)
print("Trades: \n: {}".format(trades))


