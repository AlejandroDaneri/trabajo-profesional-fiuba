import gym
import yfinance as yf
from ta import add_all_ta_features
from stable_baselines3 import PPO
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform

# Descargar datos históricos de Yahoo Finance
symbol = "AAPL"
start_date = "2022-01-01"
end_date = "2022-12-31"
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


# Funciones de compra y venta con umbral variable del RSI
def buy_signal(observation, buy_threshold):
    return observation["rsi"] < buy_threshold


def sell_signal(observation, sell_threshold):
    return observation["rsi"] > sell_threshold


# Función de recompensa simple basada en cambios de precio
def calculate_reward(previous_price, current_price, action):
    if action == "buy":
        return current_price - previous_price
    elif action == "sell":
        return previous_price - current_price
    else:
        return 0


# Crear un entorno de trading simple
class TradingEnvironment(gym.Env):
    def __init__(self, data):
        self.data = data
        self.current_step = 0
        self.total_steps = len(data) - 1

    def reset(self):
        self.current_step = 0
        return self.data.iloc[self.current_step].to_dict()

    def step(self, action):
        self.current_step += 1
        if self.current_step == self.total_steps:
            done = True
        else:
            done = False

        obs = self.data.iloc[self.current_step].to_dict()
        reward = calculate_reward(
            self.data.iloc[self.current_step - 1]["Close"],
            self.data.iloc[self.current_step]["Close"],
            action,
        )

        return obs, reward, done, {}


# Definir espacio de búsqueda para Random Search
param_dist = {
    "buy_threshold": uniform(
        loc=20, scale=60
    ),  # Umbral de compra de 20 a 80 con incrementos de 10
    "sell_threshold": uniform(
        loc=20, scale=60
    ),  # Umbral de venta de 20 a 80 con incrementos de 10
}

# Configurar el modelo base
base_model = PPO("MlpPolicy", TradingEnvironment(data), verbose=0)

# Configurar la búsqueda aleatoria
random_search = RandomizedSearchCV(
    estimator=base_model,
    param_distributions=param_dist,
    n_iter=10,  # Ajusta según el número deseado de configuraciones aleatorias
    cv=3,  # Ajusta según el número deseado de divisiones en la validación cruzada
    verbose=2,
    n_jobs=-1,
)

# Realizar la búsqueda aleatoria
random_search.fit(
    data, n_steps=10000
)  # Ajusta según la cantidad deseada de pasos de entrenamiento

# Mejores configuraciones encontradas
best_buy_threshold = random_search.best_params_["buy_threshold"]
best_sell_threshold = random_search.best_params_["sell_threshold"]
print(f"Best Buy Threshold: {best_buy_threshold}")
print(f"Best Sell Threshold: {best_sell_threshold}")
