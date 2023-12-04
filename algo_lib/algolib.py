print("Trabajo Profesional | Algo Trading | Libreria")

import pandas as pd
import numpy as np
import yfinance as yf


def get_data(ticker, start_date):
    return yf.download(ticker, auto_adjust=True, start=start_date)


def get_buy_signals(data, indicators):
    # Create a DataFrame for buy signals with the same index as the input data
    buy_signals = pd.DataFrame(index=data.index)
    buy_signals["Close"] = data.Close

    # Iterate through the specified features to generate buy signals
    for indicator in indicators:
        buy_signals[indicator.name] = indicator.calc_buy_signals()

    # Combine individual features to get an overall buy signal for each day
    buy_signals["all"] = buy_signals.all(axis=1)

    return buy_signals


def get_sell_signals(data, indicators):
    # Create a DataFrame for sell signals with the same index as the input data
    sell_signals = pd.DataFrame(index=data.index)
    sell_signals["Close"] = data.Close

    # Iterate through the specified features to generate sell signals
    for indicator in indicators:
        sell_signals[indicator.name] = indicator.calc_sell_signals()

    # Combine individual features to get an overall sell signal for each day
    sell_signals["all"] = sell_signals.all(axis=1)

    return sell_signals


def get_actions(buy_signals, sell_signals):
    # Create a DataFrame for actions with the same index as buy_signals
    actions = pd.DataFrame(index=buy_signals.index)
    actions["Close"] = buy_signals.Close

    # Define masks for buy and sell signals
    buy_mask = buy_signals["all"]
    sell_mask = sell_signals["all"]

    # Determine if it's a buy, sell, or no action day
    actions["signal"] = np.where(buy_mask, "buy", np.where(sell_mask, "sell", ""))

    # Create a new DataFrame with rows filtered for days with buy or sell signals
    trades = actions.loc[actions["signal"] != ""].copy()

    # Detect repeated signals between the current and previous rows and remove duplicates
    trades["signal"] = np.where(
        trades.signal != trades.signal.shift(), trades.signal, ""
    )

    # Filter out rows with no signal
    trades = trades.loc[trades.signal != ""].copy()

    # Handle cases where the first trade is sell or the last trade is buy
    if trades.iloc[0].loc["signal"] == "sell":
        trades = trades.iloc[1:]
    if trades.iloc[-1].loc["signal"] == "buy":
        trades = trades.iloc[:-1]

    return trades


def get_trades(actions):
    # Extract pairs for buy actions
    pairs = actions.iloc[::2].loc[:, ["Close"]].reset_index()

    # Extract odd-indexed rows for sell actions
    odds = actions.iloc[1::2].loc[:, ["Close"]].reset_index()

    # Combine buy and sell dataframes side by side
    trades = pd.concat([pairs, odds], axis=1)

    # Cumulative return calculation
    cumulative_return = 0
    trades.columns = ["buy_date", "buy_price", "sell_date", "sell_price"]

    # Calculate the trade return
    trades["return"] = trades.sell_price / trades.buy_price - 1
    trades["return"] -= cumulative_return

    # Calculate the duration of the trade in days
    trades["days"] = (trades.sell_date - trades.buy_date).dt.days

    if len(trades):
        # Classify the trade result as 'Winner' or 'Loser'
        trades["result"] = np.where(trades["return"] > 0, "Winner", "Loser")

        # Calculate the cumulative return for all trades
        trades["cumulative_return"] = (trades["return"] + 1).cumprod() - 1

    return trades


def backtesting(self, indicator="RSI", trig_buy=65, trig_sell=55):
    data.dropna(inplace=True)

    if len(trades):
        # agg_cant = trades.groupby('Nose').size()
        agg_rend = trades.groupby("resultado").mean()["rendimiento"]
        agg_tiempos = trades.groupby("resultado").sum()["dias"]
        agg_tiempos_medio = trades.groupby("resultado").mean()["dias"]

        r = pd.concat([agg_rend, agg_tiempos, agg_tiempos_medio], axis=1)
        r.columns = ["Rendimiento x Trade", "Dias Total", "Dias x Trade"]
        resumen = r.T

        try:
            t_win = r["Dias Total"]["Ganador"]
        except:
            t_win = 0

        try:
            t_loss = r["Dias Total"]["Perdedor"]
        except:
            t_loss = 0

        t = t_win + t_loss

        tea = (resultado + 1) * (365 / t) - 1 if t > 0 else 0

        metricas = {
            "rendimiento": round(resultado, 4),
            "dias in": round(t, 4),
            "TEA": round(tea, 4),
        }

    else:
        resumen = pd.DataFrame()
        metricas = {"rendimiento": 0, "dias_in": 0, "TEA": 0}
    print(actions)
    print(resumen)
    print(metricas)

    def OBV(self, n):
        data["Balance"] = np.where(
            data.Close > data.Close.shift(),
            data["Volume"],
            np.where(data.Close < data.Close.shift(), -data["Volume"], 0),
        )
        data["OBV"] = data["Balance"].rolling(n).sum()
        data["OBV_acotado"] = self.narror_indicator_by("min_dist", data["OBV"], n)
        return data

    def narror_indicator_by(self, type_, col, n):
        narrow_types = {
            "min_dist": (col - col.rolling(n).min())
            / (col.rolling(n).max() - col.rolling(n).min()),
            "z_scores_n_window": (col - col.rolling(n).mean()) / (col.rolling(n).std()),
            "z_scores_all": (col - col.mean() / col.std()),
        }
        return narrow_types.get(type_)
