from algo_lib.indicators.indicator import Indicator
from algo_lib.strategies.strategy import Strategy

from collections import Counter
import pandas as pd
import numpy as np
from typing import List, Tuple

class Basic(Strategy):
    def __init__(self, indicators: List[Indicator]):
        self.name = "BASIC"
        super().__init__(indicators)

    def train(self, historical_data):
        for indicator in self.indicators:
            indicator.calculate(historical_data)
        return

    def predict(self, new_record):
        # List to store predicted signals from each indicator
        signals = []

        # Get predicted signals from each indicator
        for indicator in self.indicators:
            signal = indicator.predict_signal(new_record)
            signals.append(signal)

        # Count the frequency of each signal
        signal_counter = Counter(signals)

        # Get the most common signal
        most_common_signal = signal_counter.most_common(1)[0][0]

        return most_common_signal

    def backtest(self, historical_data: pd.DataFrame) -> None:
        # Entrenar la estrategia con datos históricos
        self.train(historical_data)

        # Obtener señales de compra y venta
        buy_signals, sell_signals = self.get_buy_sell_signals(historical_data)

        # Obtener acciones a partir de las señales
        actions = self.get_actions(buy_signals, sell_signals)

        # Obtener trades a partir de las acciones
        trades = self.get_trades(actions)

        # Realizar análisis de backtesting
        self.analyze_backtesting(trades)

    def get_buy_sell_signals(
        self, historical_data: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Lógica para obtener señales de compra y venta
        # Asumo que tu estrategia tiene un método predict_signal similar al que mostraste
        buy_signals = pd.DataFrame(index=historical_data.index)
        sell_signals = pd.DataFrame(index=historical_data.index)

        for indicator in self.indicators:
            indicator.calculate(historical_data)
            signal = indicator.predict_signal(historical_data)
            buy_signals[indicator.name] = np.where(signal == "buy", 1, 0)
            sell_signals[indicator.name] = np.where(signal == "sell", 1, 0)

        return buy_signals, sell_signals

    def get_actions(
        self, buy_signals: pd.DataFrame, sell_signals: pd.DataFrame
    ) -> pd.DataFrame:
        # Lógica para obtener acciones a partir de las señales
        actions = pd.DataFrame(index=buy_signals.index)
        actions["Close"] = buy_signals["Close"]

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

    def get_trades(self, actions: pd.DataFrame) -> pd.DataFrame:
        # Lógica para obtener trades a partir de las acciones
        pairs = actions.iloc[::2].loc[:, ["Close"]].reset_index()
        odds = actions.iloc[1::2].loc[:, ["Close"]].reset_index()
        trades = pd.concat([pairs, odds], axis=1)
        cumulative_return = 0
        trades.columns = ["buy_date", "buy_price", "sell_date", "sell_price"]
        trades["return"] = trades.sell_price / trades.buy_price - 1
        trades["return"] -= cumulative_return
        trades["days"] = (trades.sell_date - trades.buy_date).dt.days

        if len(trades):
            trades["result"] = np.where(trades["return"] > 0, "Winner", "Loser")
            trades["cumulative_return"] = (trades["return"] + 1).cumprod() - 1

        return trades
