
from lib.trade import Trade
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance as BinanceProvider
from lib.strategies.strategy import Strategy
from utils import hydrate_strategy, timeframe_2_seconds
from common.notifications.telegram.telegram_notifications_service import notify_telegram_users
from api_client import ApiClient
import time
import sentry_sdk
import os
from typing import Dict

def init_sentry():
    env = os.getenv('ENV')
    if env != "development": 
        sentry_sdk.init(
            dsn="https://99aef705bb2355581d11e36d65ffa585@o4506996875919360.ingest.us.sentry.io/4506996882341888",
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

# get strategy from the db, and hydrate Strategy class with the data
def get_current_strategy(data_provider: BinanceProvider, api: ApiClient) -> Dict[str, Strategy]:
    WAIT_TIME_TO_CHECK_NEW_STRATEGY_IN_SECONDS = 60

    strategy = None
    while strategy is None:
        response = api.get('api/strategy/running')
        if response.status_code == 200:
            print("[main] strategy found")
            strategy = response.json()
            print(f"[main] strategy: {strategy}")
        else:
            print("[main] zero running strategies")
            time.sleep(WAIT_TIME_TO_CHECK_NEW_STRATEGY_IN_SECONDS)

    print(strategy)

    id = strategy["id"]
    indicators = strategy["indicators"]
    currencies = strategy["currencies"]
    timeframe = strategy["timeframe"]
    type = strategy["type"]
    initial_balance = strategy["initial_balance"]

    print(f"[main] initial balance: {initial_balance}")

    strategy = hydrate_strategy(type, currencies, indicators, timeframe, id)

    n_train = 200

    data = {}
    train_data = {}
    for currency in currencies:
        data[currency] = data_provider.get(currency, timeframe, n=n_train)
        train_data[currency] = data[currency].iloc[0:n_train]
        strategy[currency].prepare_data(train_data[currency])

    return strategy

# inject new tick to trade bot to detect buy and sell signals
def inject_new_tick_to_trade_bot(strategy: Dict[str, Strategy], trade_bot: TradeBot, data_provider: BinanceProvider, api: ApiClient):
    for currency in list(strategy.keys()):
        data = data_provider.get(currency, strategy[currency].get_timeframe(), n=1)
        print(f'Get: {currency} {data.index[0]}')
        trade = trade_bot.run_strategy(currency, data)
        if trade is not None:
            # trade closed: means buy and sell executed
            if trade.is_closed():
                # save closed trade
                data = {
                    "pair": trade.symbol,
                    "amount": str(trade.amount),
                    "buy": {
                        "price": str(trade.buy_order.price),
                        "timestamp": int(trade.buy_order.timestamp)
                    },
                    "sell": {
                        "price": str(trade.sell_order.price),
                        "timestamp": int(trade.sell_order.timestamp)
                    }
                }
                response = api.post('api/trade', json=data)

                # remove tmp current trade
                api.delete('api/trade/current')

                notify_telegram_users(data)
                response = api.post('api/trade/current', json=data)
                            
                # update balance to strategy doc in the db
                current_balance = trade_bot.get_balance()
                print(f"Current balance: {current_balance}")
                api.put(f'api/strategy/{id}/balance', json={
                    "current_balance": str(current_balance)
                })
            else:
                # trade current: buy executed but not sell yet
                data = {
                    "pair": trade.symbol,
                    "amount": str(trade.amount),
                    "buy": {
                        "price": str(trade.buy_order.price),
                        "timestamp": int(trade.buy_order.timestamp)
                    }
                }
                response = api.post('api/trade/current', json=data)

    time.sleep(timeframe_2_seconds(strategy[currency].get_timeframe()))                  
    print("\n")
