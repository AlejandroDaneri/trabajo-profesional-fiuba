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

# Descargar datos históricos de Yahoo Finance
symbol = "BTC-USD"
start_date = "2020-01-01"
end_date = "2023-12-01"
data = yf.download(symbol, start=start_date, end=end_date)

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
    def __init__(self, data):
        self.data = data
        self.current_step = 0
        self.total_steps = len(data) - 1
        self.exchange = Dummy()
        self.trades = []
        # Define el espacio de observación que incluye el RSI y MACD
        self.observation_space = gym.spaces.Box(
            low=np.array([0, -np.inf]),  # Cambia según el rango real de tu MACD
            high=np.array([100, np.inf]),  # Cambia según el rango real de tu MACD
            shape=(2,),  # Ajusta según la cantidad de indicadores en tu observación
            dtype=np.float32,
        )
        self.action_space = gym.spaces.Discrete(len(action_enum))

        self._action_dict = {
            0: Action.BUY,
            1: Action.SELL,
            2: Action.HOLD,
        }

    def reset(self, **kwargs):
        self.current_step = 0
        self.exchange = Dummy()
        self.trades = []
        obs = np.array(
            [
                self.data.iloc[self.current_step]["rsi"],
                self.data.iloc[self.current_step]["macd"],
            ],
            dtype=np.float32,
        )
        return obs, {}

    def _execute_trade(self, action: Action, symbol, amount: float, price: float):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, price)

            self.exchange.place_order(trade)
            self.trades.append(trade)

    def get_profit(self):
        return self.exchange.get_profit()

    def _run_step(self, action, actual_data):  # based on run strategy trade bot
        if self.trades:
            last_action = self.trades[-1].action
            last_trade_price = self.trades[-1].price_per_unit
            asset_last_value = actual_data["Close"]
            # Check for stop-loss condition before executing a sell order
            if last_action == Action.BUY and asset_last_value < last_trade_price * (
                1 - 0.2
            ):
                print("Stop-loss triggered. Selling...")
                self._execute_trade(
                    Action.SELL,
                    symbol,
                    self.exchange.portfolio[symbol],
                    asset_last_value,
                )
                return  # Stop further execution after stop-loss triggered

        buy_condition = action == Action.BUY and (
            not self.trades or last_action == Action.SELL
        )
        if action == Action.BUY and not (not self.trades or last_action == Action.SELL):
            raise Exception("fail")
        sell_condition = (
            self.trades and action == Action.SELL and last_action == Action.BUY
        )
        if self.trades and not (action == Action.SELL and last_action == Action.BUY):
            raise Exception("fail")
        asset_last_value = actual_data["Close"]

        if buy_condition:
            max_buy_amount = 1 * self.exchange.balance / asset_last_value
            self._execute_trade(Action.BUY, symbol, max_buy_amount, asset_last_value)

        elif sell_condition:
            max_sell_amount = self.exchange.portfolio[symbol] * 1
            self._execute_trade(Action.SELL, symbol, max_sell_amount, asset_last_value)

    def step(self, action):
        self.current_step += 1
        action_str = self._action_dict[int(action)]

        if self.current_step == self.total_steps:
            terminated = True
        else:
            terminated = False

        obs = np.array(
            [
                self.data.iloc[self.current_step]["rsi"],
                self.data.iloc[self.current_step]["macd"],
            ],
            dtype=np.float32,
        )

        try:
            self._run_step(action_str, self.data.iloc[self.current_step])
            reward = self.exchange.get_profit()
        except Exception:
            reward = -1e-100

        return obs, reward, terminated, terminated, {}


first_records = data.iloc[:-250]
last_records = data.iloc[-250:]

models_dir = "models/QDN"
if not os.path.exists(models_dir):
    os.makedirs(models_dir)
    env = TradingEnvironment(first_records)
    data_l = len(first_records) - 1

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
    model.save(f"{models_dir}/trained")
else:
    env = TradingEnvironment(last_records)
    data_l = len(last_records) - 1
    model = DQN.load(f"{models_dir}/trained.zip", env)

total_rewards = []
obs, _ = env.reset()
for _ in range(data_l):
    action, _ = model.predict(obs)
    new_obs, reward, done, _, _ = env.step(action)
    total_rewards.append(reward)

avg_reward = np.mean(total_rewards)
print("AVG", avg_reward)
