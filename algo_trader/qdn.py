import os
import gymnasium as gym
import yfinance as yf
from ta import add_all_ta_features
import numpy as np
from lib.trade import Trade
from lib.exchanges.dummy import Dummy
from stable_baselines3 import DQN
from lib.actions import Action
import numpy as np

ticker = "BTC-USD"
start_date = "2020-01-01"
end_date = "2023-12-01"
save_dir = "models/QDN/multi"
filename = "rsi_macd2"

data = yf.download(ticker, start=start_date, end=end_date)

# Calcular indicadores técnicos con la biblioteca TA-Lib
data = add_all_ta_features(
    data,
    open="Open",
    high="High",
    low="Low",
    close="Close",
    volume="Volume",
    fillna=True,
)
rsi_column = "momentum_rsi"
macd_column = "trend_macd"
# Renombrar la columna a 'rsi'
data.rename(columns={rsi_column: "rsi"}, inplace=True)
data.rename(columns={macd_column: "macd"}, inplace=True)

rsi_values = data["rsi"]

action_enum = Action


class TradingEnvironment(gym.Env):
    def __init__(self, data, indicator_columns, symbol):
        self.data = data
        self.current_step = 0
        self.total_steps = len(data) - 1
        self.exchange = Dummy()
        self.trades = []
        self.indicator_columns = indicator_columns
        self.stop_loss_ratio = 0.2
        self.strategy.investment_ratio = 1
        self.symbol = symbol

        self.observation_space = gym.spaces.Box(
            low=np.array([0, -np.inf]),
            high=np.array([100, np.inf]),
            shape=(len(self.indicator_columns),),
            dtype=np.float32,
        )
        self.action_space = gym.spaces.Discrete(len(action_enum))

        self._action_dict = {
            0: Action.BUY,
            1: Action.SELL,
            2: Action.HOLD,
        }

    def _get_obs(self):
        return np.array(
            [self.data.iloc[self.current_step][col] for col in self.indicator_columns],
            dtype=np.float32,
        )

    def reset(self, **kwargs):
        self.current_step = 0
        self.exchange = Dummy()
        self.trades = []
        obs = self._get_obs()
        return obs, {}

    def _execute_trade(self, action: Action, symbol, amount: float, price: float):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, price)

            self.exchange.place_order(trade)
            self.trades.append(trade)

    def get_profit(self):
        return self.exchange.get_profit()

    def trigger_action(self, action, asset_last_value):
        ##TODO: Same function in trade_bot, make changes to both until the refactoring is done.
        if self.trades:
            last_action = self.trades[-1].action
            last_trade_price = self.trades[-1].price_per_unit

            # Check for stop-loss condition before executing a sell order
            if last_action == Action.BUY and asset_last_value < last_trade_price * (
                1 - self.stop_loss_ratio
            ):
                print("Stop-loss triggered. Selling...")
                self._execute_trade(
                    Action.SELL,
                    self.symbol,
                    self.exchange.portfolio[self.symbol],
                    asset_last_value,
                )
                return  # Stop further execution after stop-loss triggered

        buy_condition = not self.trades or last_action == Action.SELL
        sell_condition = self.trades and last_action == Action.BUY

        if action == Action.BUY and not buy_condition:
            raise Exception("Need to sell first")

        if action == Action.SELL and not sell_condition:
            raise Exception("Need to buy firts")

        if action == Action.BUY and buy_condition:
            max_buy_amount = (
                self.strategy.investment_ratio
                * self.exchange.balance
                / asset_last_value
            )
            self._execute_trade(
                Action.BUY, self.symbol, max_buy_amount, asset_last_value
            )

        elif action == Action.SELL and sell_condition:
            max_sell_amount = (
                self.exchange.portfolio[self.symbol] * self.strategy.investment_ratio
            )
            self._execute_trade(
                Action.SELL, self.symbol, max_sell_amount, asset_last_value
            )

    def step(self, action):
        self.current_step += 1
        action_str = self._action_dict[int(action)]

        if self.current_step == self.total_steps:
            terminated = True
        else:
            terminated = False

        obs = self._get_obs()

        try:
            self.trigger_action(action_str, self.data.iloc[self.current_step]["Close"])
            reward = self.exchange.get_profit()
        except Exception:
            reward = -1e-100

        return obs, reward, terminated, terminated, {}


train_records = data.iloc[:-250]
test_records = data.iloc[-250:]

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

if not os.path.exists(save_dir + "/" + filename):
    env = TradingEnvironment(train_records, ["rsi", "macd"])
    data_l = len(train_records) - 1

    model = DQN(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=4e-3,
        gradient_steps=8,
        gamma=0.99,
        exploration_fraction=0.2,
        exploration_final_eps=0.07,
    )
    model.learn(total_timesteps=1.2e5)
    model.save(f"{save_dir}/{filename}")

else:
    env = TradingEnvironment(test_records, ticker, ["rsi", "macd"])
    data_l = len(test_records) - 1
    model = DQN.load(f"{save_dir}/{filename}.zip", env)

total_rewards = []
obs, _ = env.reset()
for _ in range(data_l):
    action, _ = model.predict(obs)
    new_obs, reward, done, _, _ = env.step(action)
    total_rewards.append(reward)

avg_reward = np.mean(total_rewards)
print("AVG", avg_reward)
