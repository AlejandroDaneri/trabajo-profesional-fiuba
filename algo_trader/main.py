print("Trabajo Profesional | Algo Trading | Trader")

from lib.trade_bot import TradeBot
from lib.providers.binance import Binance as BinanceProvider
from lib.exchanges.binance import Binance as BinanceExchange
from api_client import ApiClient

from main_utils import init_sentry, get_current_strategy, inject_new_tick_to_trade_bot

init_sentry()

def main():
    data_provider = BinanceProvider()
    exchange = BinanceExchange()
    api = ApiClient()

    strategy = get_current_strategy(data_provider, api)
    trade_bot = TradeBot(strategy, exchange)

    while True:
        strategy_id = list(strategy.values())[0].get_id()
        response = api.get(f'api/strategy/{strategy_id}/is_running')
        is_running = response.json()
        print(f"[main] strategy id: {strategy_id}, running: {is_running}")
        if is_running:
            inject_new_tick_to_trade_bot(strategy, trade_bot, data_provider, api)
        else:
            strategy = get_current_strategy(data_provider, api)
            trade_bot = TradeBot(strategy, exchange)
     
if __name__ == "__main__":
    main()
