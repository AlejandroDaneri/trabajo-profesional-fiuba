import gymnasium as gym
import yfinance as yf
from ta import add_all_ta_features
from stable_baselines3 import PPO
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform
import numpy as np
from lib.trade import Trade
from lib.exchanges.dummy import Dummy
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
import time
from lib.actions import Action
import numpy as np


# Descargar datos históricos de Yahoo Finance
symbol = "SOL-USD"
start_date = "2022-01-01"
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

# Renombrar la columna a 'rsi'
data.rename(columns={rsi_column: "rsi"}, inplace=True)

# Ahora puedes referenciarla simplemente como 'rsi'
rsi_values = data["rsi"]


# Funciones de compra y venta con umbral variable del RSI
# def buy_signal(observation, buy_threshold):
#     return observation["rsi"] < buy_threshold


# def sell_signal(observation, sell_threshold):
#     return observation["rsi"] > sell_threshold


# Función de recompensa simple basada en cambios de precio
# def calculate_reward(previous_price, current_price, action):
#     if action == Action.BUY:
#         return current_price - previous_price
#     elif action == Action.SELL:
#         return previous_price - current_price
#     elif action == Action.HOLD:
#         return 0


action_enum = Action


class TradingEnvironment(gym.Env):
    def __init__(self, data):
        self.data = data
        self.current_step = 0
        self.total_steps = len(data) - 1
        self.exchange = Dummy()
        self.trades = []
        # Define el espacio de observación que incluye el RSI
        self.observation_space = gym.spaces.Box(
            low=0, high=100, shape=(1,), dtype=np.float32
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
        obs = np.array([self.data.iloc[self.current_step]["rsi"]], dtype=np.float32)
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

        obs = np.array([self.data.iloc[self.current_step]["rsi"]], dtype=np.float32)
        try:
            self._run_step(action_str, self.data.iloc[self.current_step])
            reward = self.exchange.get_profit()
        except Exception:
            reward = -1e-100
            terminated = True

        if reward > 0:
            print("reward", reward, len(self.trades))

        return obs, reward, terminated, terminated, {}


# class QLearningAgent:
#     def __init__(
#         self,
#         n_actions,
#         n_states,
#         learning_rate=0.1,
#         discount_factor=0.9,
#         exploration_prob=0.2,
#     ):
#         self.n_actions = n_actions
#         self.n_states = n_states
#         self.learning_rate = learning_rate
#         self.discount_factor = discount_factor
#         self.exploration_prob = exploration_prob

#         # Inicializa la tabla Q con ceros
#         self.Q = np.zeros((n_states, n_actions))

#     def select_action(self, state):
#         # Selección de acción con epsilon-greedy para la exploración
#         if np.random.rand() < self.exploration_prob:
#             return np.random.choice(self.n_actions)
#         else:
#             return np.argmax(self.Q[state, :])

#     def update_q_values(self, state, action, reward, next_state):
#         # Actualiza los valores Q usando la ecuación de Bellman
#         best_next_action = np.argmax(self.Q[next_state, :])
#         self.Q[state, action] += self.learning_rate * (
#             reward
#             + self.discount_factor * self.Q[next_state, best_next_action]
#             - self.Q[state, action]
#         )


# # Crear el agente Q-learning
# n_actions = len(Action)
# n_states = (
#     1  # Número de estados en tu entorno (por ejemplo, número de indicadores técnicos)
# )
# agent = QLearningAgent(n_actions, n_states)
# env = TradingEnvironment(data)

# obs = env.reset()
# # Bucle de interacción con el entorno (puedes personalizar esto según tus necesidades)
# for _ in range(len(data) - 1):
#     # Obtener el estado actual del entorno (en este caso, solo el RSI)
#     state = np.array([obs["rsi"]])

#     # Seleccionar una acción utilizando el agente Q-learning
#     action = agent.select_action(state)
#     # Ejecuta la acción en el entorno
#     new_obs, reward, done, _ = env.step(action)

#     # Obtener el nuevo estado del entorno
#     next_state = np.array([new_obs["rsi"]])

#     # Actualizar los valores Q del agente
#     agent.update_q_values(state, action, reward, next_state)

#     # Actualizar el estado actual
#     state = next_state
#     # Sale del bucle si el episodio ha terminado
#     if done:
#         break

# # Cierra el entorno al final
# env.close()


# # Crear el entorno
env = TradingEnvironment(data)
# # Crear el modelo DQN
# model = DQN(
#     "MlpPolicy",
#     env,
#     verbose=1,
#     learning_rate=4e-3,
#     gradient_steps=8,
#     gamma=0.99,
#     exploration_fraction=0.2,
#     exploration_final_eps=0.07,
# )

# # Entrenar el modelo (puedes ajustar el número de pasos de entrenamiento)
# model.learn(total_timesteps=1.2e5)

# # Bucle de interacción con el entorno

# time.sleep(10)
# test_length = 10000
# for episode in range(test_length):
#     obs, _ = env.reset()
#     # Seleccionar una acción utilizando el modelo DQN
#     action, _ = model.predict(obs)

#     # Ejecutar la acción en el entorno
#     new_obs, reward, done, _, _ = env.step(action)

#     # Actualizar la observación actual
#     obs = new_obs

#     # Salir del bucle si el episodio ha terminado
#     if done:
#         break

# Define el espacio de búsqueda
param_dist = {
    "learning_rate": np.logspace(-5, -2, num=1000),
    "gradient_steps": [4, 8, 16, 32],
}

# Almacena los resultados de la búsqueda
results = []

# Número de iteraciones de búsqueda aleatoria
n_iterations = 10

for _ in range(n_iterations):
    # Muestrea aleatoriamente del espacio de búsqueda
    params = {
        "learning_rate": np.random.choice(param_dist["learning_rate"]),
        "gradient_steps": np.random.choice(param_dist["gradient_steps"]),
    }

    # Crea el modelo con los parámetros seleccionados
    model = DQN(
        "MlpPolicy",
        env,
        verbose=0,
        learning_rate=params["learning_rate"],
        gradient_steps=params["gradient_steps"],
        gamma=0.99,
        exploration_fraction=0.2,
        exploration_final_eps=0.07,
    )

    # Entrenar el modelo (puedes ajustar el número de pasos de entrenamiento)
    model.learn(total_timesteps=1.2e5)

    # Evaluar el modelo y almacenar resultados
    test_length = 10000
    total_rewards = []
    for _ in range(test_length):
        obs, _ = env.reset()
        action, _ = model.predict(obs)
        new_obs, reward, done, _, _ = env.step(action)
        total_rewards.append(reward)

    avg_reward = np.mean(total_rewards)
    results.append({"params": params, "avg_reward": avg_reward})

# Ordenar los resultados por recompensa promedio
results = sorted(results, key=lambda x: x["avg_reward"], reverse=True)

# Obtener los mejores hiperparámetros
best_params = results[0]["params"]
print("Mejores hiperparámetros:", best_params)
