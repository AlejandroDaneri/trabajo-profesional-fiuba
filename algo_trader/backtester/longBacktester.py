from lib.strategies.strategy import Strategy
import pandas as pd
import numpy as np
from typing import Tuple

class LongBacktester:
    def __init__(self, strategy: Strategy, initial_balance: float, fixed_commission: float=0.005, variable_commission_rate: float=0.005):        
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.fixed_commission = fixed_commission
        self.variable_commission_rate = variable_commission_rate

    def backtest(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
        trades, final_balance = self._execute_backtest(historical_data)

        return trades, final_balance

    def _execute_backtest(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
        buy_signals, sell_signals = self._get_buy_sell_signals(historical_data)

        actions = self._get_actions(buy_signals, sell_signals)
        historical_data['signal'] = actions['signal'] #FIXME

        trades = self._get_trades(actions)

        final_balance = self._calculate_final_balance(historical_data, trades, self.initial_balance)

        return trades, final_balance

    def _get_buy_sell_signals(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        buy_signals = pd.DataFrame(index=historical_data.index)
        sell_signals = pd.DataFrame(index=historical_data.index)
        buy_signals["Close"] = historical_data["Close"]
        sell_signals["Close"] = historical_data["Close"]

        for indicator in self.strategy.indicators:
            indicator.calculate(historical_data)
            buy_signals[indicator.name] = np.where(indicator.calc_buy_signals(), 1, 0)
            sell_signals[indicator.name] = np.where(indicator.calc_sell_signals(), 1, 0)

        return buy_signals, sell_signals

    def _get_actions(self, buy_signals: pd.DataFrame, sell_signals: pd.DataFrame) -> pd.DataFrame:
        actions = pd.DataFrame(index=buy_signals.index)
        actions["Close"] = buy_signals["Close"]

        buy_mask = buy_signals.all(axis=1)
        sell_mask = sell_signals.all(axis=1)

        actions["signal"] = np.where(buy_mask, "buy", np.where(sell_mask, "sell", ""))

        trades = actions.loc[actions["signal"] != ""].copy()
        trades["signal"] = np.where(
            trades.signal != trades.signal.shift(), trades.signal, ""
        )
        trades = trades.loc[trades.signal != ""].copy()
        if not trades.empty: 
            if len(trades) > 1:
                if trades.iloc[0].loc["signal"] == "sell":
                    trades = trades.iloc[1:]
                if trades.iloc[-1].loc["signal"] == "buy":
                    trades = trades.iloc[:-1]
            else:
                if trades.iloc[0].loc["signal"] == "sell":
                    trades = trades.iloc[1:]

        return trades

    def _get_trades(self, actions: pd.DataFrame) -> pd.DataFrame:
        pairs = actions.iloc[::2].loc[:, ["Close"]].reset_index()
        odds = actions.iloc[1::2].loc[:, ["Close"]].reset_index()
        trades = pd.concat([pairs, odds], axis=1)
        trades.columns = ["buy_date", "buy_price", "sell_date", "sell_price"]

        trades["fixed_commission"] = self.fixed_commission
        trades["variable_commission"] = trades["buy_price"] * self.variable_commission_rate

        trades["buy_price"] += trades["fixed_commission"] + trades["variable_commission"]
        trades["sell_price"] -= trades["fixed_commission"] + trades["variable_commission"]

        trades["return"] = trades.sell_price / trades.buy_price - 1

        cumulative_return = (1 + trades["return"]).cumprod() - 1
        trades["cumulative_return"] = cumulative_return

        trades["result"] = np.where(trades["return"] > 0, "Winner", "Loser")

        return trades

    def _calculate_final_balance(self, data, trades, starting_capital=10000):
        if len(trades) == 0:
            return starting_capital

        cumulative_return = trades['cumulative_return'].iloc[-1]

        last_signal = data['signal'].iloc[-1]
        if last_signal == 'buy':
            current_price = data['Close'].iloc[-1]
            open_trade_price = data['Close'].iloc[-2]  
            unrealized_pnl = (current_price / open_trade_price) - 1
        else:
            unrealized_pnl = 0  

        final_balance = starting_capital * (1 + cumulative_return + unrealized_pnl)

        return final_balance
