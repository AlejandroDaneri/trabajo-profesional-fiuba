import tensorflow as tf
from keras import __version__

tf.keras.__version__ = __version__

from collections import OrderedDict
from datetime import datetime
import os
import time
import gymnasium as gym
import numpy as np
from lib.indicators.rsi import RSI
from lib.providers.binance import Binance
from lib.trade import Trade
from lib.exchanges.dummy import Dummy
from lib.actions import Action
from typing import List
from lib.indicators.indicator import Indicator
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory


ticker = "BTCUSDT"
start_date = "2020-01-01"
end_date = "2023-12-01"
save_dir = "models/QDN/multi"
filename = "qdn_rt"

provider = Binance()
print("get data")
data = provider.get_data_from(ticker, "2024-01-08")
print(len(data))
print("finish data")

action_enum = Action


class TradingEnvironment(gym.Env):
    def __init__(self, data, indicators: List[Indicator], symbol):
        self.data = data
        self.current_step = 0
        self.total_steps = len(data) - 1
        self.exchange = Dummy()
        self.trades = []
        self.indicators = indicators
        self.stop_loss_ratio = 0.2
        self.investment_ratio = 1
        self.symbol = symbol

        self.observation_space = gym.spaces.Dict(
            {
                "predictions": gym.spaces.MultiDiscrete(
                    [len(action_enum)] * len(self.indicators)
                ),
                "close": gym.spaces.Box(low=0, high=np.inf, shape=(), dtype=np.float32),
            }
        )
        self.action_space = gym.spaces.Discrete(len(action_enum))

        self._int_to_action = {
            0: Action.HOLD,
            1: Action.SELL,
            2: Action.BUY,
        }

        self._action_to_int = {
            Action.HOLD: 0,
            Action.SELL: 1,
            Action.BUY: 2,
        }

    def step(self, action, obs):
        self.current_step += 1
        action_str = self._int_to_action[int(action)]

        if self.current_step == self.total_steps:
            terminated = True
        else:
            terminated = False

        try:
            self.trigger_action(action_str, obs["close"])
            reward = self.exchange.get_profit()
        except Exception:
            reward = -1e-100

        obs = self._get_obs()
        return obs, reward, terminated, terminated, {}

    def _get_obs(self):
        print("waiting 1 secs")
        time.sleep(1)
        data = self.provider.get_latest_data(ticker)
        ind_preds = np.array(
            [
                self._action_to_int[indicator.predict_signal(data)]
                for indicator in self.indicators
            ],
            dtype=int,
        )
        obs = OrderedDict(
            [
                ("close", np.array(data["Close"][0], dtype=np.float32)),
                ("predictions", ind_preds),
            ]
        )
        print(obs)
        return obs

    def reset(self, **kwargs):
        self.provider = Binance()
        actual_date = datetime.now().strftime("%Y-%m-%d")
        data = provider.get_data_from("BTCUSDT", actual_date)
        for indicator in self.indicators:
            indicator.calculate(data)
        self.current_step = 0
        self.exchange = Dummy()
        self.trades = []
        obs = self._get_obs()
        return obs, {}

    def execute_trade(self, action: Action, symbol, amount: float, price: float):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, price)
            try:
                self.exchange.place_order(trade)
                self.trades.append(trade)
            except Exception as e:
                print(f"Error executing trade: {e}")

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
                self.execute_trade(
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
                self.investment_ratio * self.exchange.balance / asset_last_value
            )
            self.execute_trade(
                Action.BUY, self.symbol, max_buy_amount, asset_last_value
            )

        elif action == Action.SELL and sell_condition:
            max_sell_amount = (
                self.exchange.portfolio[self.symbol] * self.investment_ratio
            )
            self.execute_trade(
                Action.SELL, self.symbol, max_sell_amount, asset_last_value
            )


class TestingEnvironment(gym.Env):
    def __init__(self, data, indicators: List[Indicator], symbol):
        self.data = data
        self.current_step = 100
        self.total_steps = len(data) - 1
        self.exchange = Dummy()
        self.trades = []
        self.indicators = indicators
        self.stop_loss_ratio = 0.2
        self.investment_ratio = 1
        self.symbol = symbol

        self.observation_space = gym.spaces.Dict(
            {
                "predictions": gym.spaces.MultiDiscrete(
                    [len(action_enum)] * len(self.indicators), dtype=int
                ),
                "close": gym.spaces.Box(low=0, high=np.inf, shape=(), dtype=np.float32),
            }
        )

        self.action_space = gym.spaces.Discrete(len(action_enum))

        self._int_to_action = {
            0: Action.HOLD,
            1: Action.SELL,
            2: Action.BUY,
        }

        self._action_to_int = {
            Action.HOLD: 0,
            Action.SELL: 1,
            Action.BUY: 2,
        }

    def step(self, action_int):
        self.current_step += 1
        action_str = self._int_to_action[int(action_int)]

        if self.current_step == self.total_steps:
            terminated = True
        else:
            terminated = False

        try:
            self.trigger_action(
                action_str, self.data.iloc[self.current_step - 1]["Close"]
            )
            reward = self.exchange.get_profit()
        except Exception:
            reward = -1e-100

        obs = self._get_obs()

        return obs, reward, terminated, terminated, {}

    def _get_obs(self):
        data = self.data.iloc[self.current_step - 1]
        ind_preds = np.array(
            [
                self._action_to_int[indicator.predict_signal(data)]
                for indicator in self.indicators
            ],
            dtype=int,
        )
        obs = OrderedDict(
            [
                ("close", np.array(data["Close"], dtype=np.float32)),
                ("predictions", ind_preds),
            ]
        )
        print(obs)
        return obs

    def reset(self, **kwargs):
        self.provider = Binance()
        self.current_step = 100
        for indicator in self.indicators:
            indicator.calculate(data[: self.current_step - 1])
        self.exchange = Dummy()
        self.trades = []
        obs = self._get_obs()
        return obs, {}

    def execute_trade(self, action: Action, symbol, amount: float, price: float):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, price)
            try:
                self.exchange.place_order(trade)
                self.trades.append(trade)
            except Exception as e:
                print(f"Error executing trade: {e}")

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
                self.execute_trade(
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
                self.investment_ratio * self.exchange.balance / asset_last_value
            )
            self.execute_trade(
                Action.BUY, self.symbol, max_buy_amount, asset_last_value
            )

        elif action == Action.SELL and sell_condition:
            max_sell_amount = (
                self.exchange.portfolio[self.symbol] * self.investment_ratio
            )
            self.execute_trade(
                Action.SELL, self.symbol, max_sell_amount, asset_last_value
            )


# class TestingEnvironment(gym.Env):
#     def __init__(self, data, indicator_columns, symbol):
#         self.data = data
#         self.current_step = 0
#         self.total_steps = len(data) - 1
#         self.exchange = Dummy()
#         self.trades = []
#         self.indicator_columns = indicator_columns
#         self.stop_loss_ratio = 0.2
#         self.strategy.investment_ratio = 1
#         self.symbol = symbol

#         self.observation_space = gym.spaces.Box(
#             low=np.array([0, -np.inf]),
#             high=np.array([100, np.inf]),
#             shape=(len(self.indicator_columns),),
#             dtype=np.float32,
#         )
#         self.action_space = gym.spaces.Discrete(len(action_enum))

#         self._action_dict = {
#             0: Action.BUY,
#             1: Action.SELL,
#             2: Action.HOLD,
#         }

#     def _get_obs(self):
#         return np.array(
#             [self.data.iloc[self.current_step][col] for col in self.indicator_columns],
#             dtype=np.float32,
#         )

#     def reset(self, **kwargs):
#         self.current_step = 0
#         self.exchange = Dummy()
#         self.trades = []
#         obs = self._get_obs()
#         return obs, {}

#     def execute_trade(self, action: Action, symbol, amount: float, price: float):
#         if action != Action.HOLD:
#             trade = Trade(action, symbol, amount, price)
#             try:
#                 self.exchange.place_order(trade)
#                 self.trades.append(trade)
#             except Exception as e:
#                 print(f"Error executing trade: {e}")

#     def get_profit(self):
#         return self.exchange.get_profit()

#     def trigger_action(self, action, asset_last_value):
#         ##TODO: Same function in trade_bot, make changes to both until the refactoring is done.
#         if self.trades:
#             last_action = self.trades[-1].action
#             last_trade_price = self.trades[-1].price_per_unit

#             # Check for stop-loss condition before executing a sell order
#             if last_action == Action.BUY and asset_last_value < last_trade_price * (
#                 1 - self.stop_loss_ratio
#             ):
#                 print("Stop-loss triggered. Selling...")
#                 self.execute_trade(
#                     Action.SELL,
#                     self.symbol,
#                     self.exchange.portfolio[self.symbol],
#                     asset_last_value,
#                 )
#                 return  # Stop further execution after stop-loss triggered

#         buy_condition = not self.trades or last_action == Action.SELL
#         sell_condition = self.trades and last_action == Action.BUY

#         if action == Action.BUY and not buy_condition:
#             raise Exception("Need to sell first")

#         if action == Action.SELL and not sell_condition:
#             raise Exception("Need to buy firts")

#         if action == Action.BUY and buy_condition:
#             max_buy_amount = (
#                 self.strategy.investment_ratio
#                 * self.exchange.balance
#                 / asset_last_value
#             )
#             self.execute_trade(
#                 Action.BUY, self.symbol, max_buy_amount, asset_last_value
#             )

#         elif action == Action.SELL and sell_condition:
#             max_sell_amount = (
#                 self.exchange.portfolio[self.symbol] * self.strategy.investment_ratio
#             )
#             self.execute_trade(
#                 Action.SELL, self.symbol, max_sell_amount, asset_last_value
#             )

#     def step(self, action):
#         self.current_step += 1
#         action_str = self._action_dict[int(action)]

#         if self.current_step == self.total_steps:
#             terminated = True
#         else:
#             terminated = False

#         obs = self._get_obs()

#         try:
#             self.trigger_action(action_str, self.data.iloc[self.current_step]["Close"])
#             reward = self.exchange.get_profit()
#         except Exception:
#             reward = -1e-100

#         return obs, reward, terminated, terminated, {}


# train_records = data.iloc[:-250]
# test_records = data.iloc[-250:]
rsi_indicator = RSI(70, 30, 14)
indicators = [rsi_indicator]

# if not os.path.exists(save_dir):
#     os.makedirs(save_dir)
import torch as th

# Assuming your environment is 'env'

# #     if not os.path.exists(save_dir + "/" + filename):
env = TestingEnvironment(data, indicators, ticker)
# agent = DQN(
#     "MultiInputPolicy",
#     env,
#     verbose=1,
#     learning_rate=0.0001,
#     gradient_steps=8,
#     gamma=0.95,
#     exploration_fraction=0.2,
#     exploration_final_eps=0.1,
#     buffer_size=128,
# )

# agent.learn(total_timesteps=1.2e2, progress_bar=True)
# # agent.save(f"{save_dir}/{filename}")

# total_rewards = []
env_t = TradingEnvironment(data, indicators, ticker)

# # model = DQN.load(f"{save_dir}/{filename}.zip", env)
# obs, _ = env_t.reset()


# while True:
#     action, _ = agent.predict(obs)
#     print(action)
#     new_obs, reward, done, _, _ = env_t.step(0, obs)
#     total_rewards.append(reward)
#     avg_reward = np.mean(total_rewards)
#     print("AVG", avg_reward)


# Construir un modelo simple
model = Sequential()
model.add(Flatten(input_shape=(1, env.observation_space.shape[0])))
model.add(Dense(24, activation="relu"))
model.add(Dense(24, activation="relu"))
model.add(Dense(env.action_space.n, activation="linear"))

# Configurar el agente DQN
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(
    model=model,
    memory=memory,
    policy=policy,
    nb_actions=env.action_space.n,
    nb_steps_warmup=10,
    target_model_update=1e-2,
)
dqn.compile(Adam(learning_rate=1e-3), metrics=["mae"])

# Entrenamiento
dqn.fit(env, nb_steps=5000, visualize=False, verbose=2)

# Probar el modelo
dqn.test(env_t, nb_episodes=5, visualize=False)
