from lib.strategies.strategy import Strategy
import pandas as pd
import numpy as np
from typing import Tuple

class SpotBacktester:
    def __init__(self, strategy: Strategy, initial_balance: float, fixed_commission: float=0.005, variable_commission_rate: float=0.005):        
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.fixed_commission = fixed_commission
        self.variable_commission_rate = variable_commission_rate

    def backtest(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
        trades, final_balance = self.execute_backtest(historical_data)
        return trades, final_balance

    def execute_backtest(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
        buy_signals, sell_signals = self.strategy.get_buy_sell_signals(historical_data)

        actions = self._get_actions(buy_signals, sell_signals)
        historical_data['signal'] = actions['signal'] 

        trades = self._get_trades(actions)
        self.payoff= self._event_drive(historical_data)
        final_balance = self._calculate_final_balance(historical_data, trades, self.initial_balance)

        return trades, final_balance

    # def _get_buy_sell_signals(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    #     buy_signals = pd.DataFrame(index=historical_data.index)
    #     sell_signals = pd.DataFrame(index=historical_data.index)
    #     buy_signals["Close"] = historical_data["Close"]
    #     sell_signals["Close"] = historical_data["Close"]

    #     for indicator in self.strategy.indicators:
    #         indicator.calculate(historical_data)
    #         buy_signals[indicator.name] = np.where(indicator.calc_buy_signals(), 1, 0)
    #         sell_signals[indicator.name] = np.where(indicator.calc_sell_signals(), 1, 0)

    #     return buy_signals, sell_signals

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
        trades.columns = ["entry_date", "entry_price", "output_date", "output_price"]

        trades["fixed_commission"] = self.fixed_commission
        trades["variable_commission"] = trades["entry_price"] * self.variable_commission_rate

        trades["entry_price"] += trades["fixed_commission"] + trades["variable_commission"]
        trades["output_price"] -= trades["fixed_commission"] + trades["variable_commission"]

        trades["return"] = trades.output_price / trades.entry_price - 1

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
    
    def _event_drive(self,df): 
        df["pct_change"]=df['Close'].pct_change() 
        signals=df['signal'].tolist()
        pct_changes =df['pct_change'].tolist()

        total = len(signals) 
        i, results = 1, [0]

        while i<total:

            if signals[i-1] == 'buy':
                j=i
                while j<total:
                    results.append(pct_changes[j])
                    j +=1
                    if signals[j-1]=="sell":
                        i=j
                        break
                    if j == total:
                        i=j
                        print("Compra abierta")
                        break

            else:
                results.append(0)
                i +=1

        result = pd.concat([df,pd.Series(data=results,index=df.index)],axis=1)
        result.columns.values[-1] ="strategy"
        result=result.iloc[:,-2:].add(1).cumprod()

        self.linear_returns = result['strategy']
        self.benchmark = result['pct_change']
        self.log_returns = np.log(self.linear_returns /self.linear_returns.shift())
        self.benchmark_log_returns = np.log(self.benchmark /self.benchmark.shift())

        self.returns = self.linear_returns.pct_change()
        self.benchmark_returns = self.benchmark.pct_change()
        return result
