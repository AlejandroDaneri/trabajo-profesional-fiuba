from lib.constants.timeframe import *
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

FACTOR = {
    '1m': 60,
    '5m': 60 * 5,
    '15m': 60 * 15,
    '1h': 60 * 60,
    '4h': 60 * 60 * 4,
    '1d': 60 * 60 * 24
}

def get_delta(timeframe: str):
    DELTA = {
        '1m': timedelta(minutes=1),
        '5m': timedelta(minutes=5),
        '15m': timedelta(minutes=15),
        '1h': timedelta(hours=1),
        '4h': timedelta(hours=4),
        '1d': timedelta(days=1)
    }
    return DELTA[timeframe]

def generate_date_range(start_date, end_date, timeframe):
    start = datetime.strptime(start_date, DATE_FORMAT[timeframe])
    end = datetime.strptime(end_date, DATE_FORMAT[timeframe])
    delta = get_delta(timeframe)
    dates = []
    current_date = start
    while current_date <= end:
        dates.append(current_date.strftime(DATE_FORMAT[timeframe]))
        current_date += delta
    return dates

def loc(data: pd.DataFrame, date: datetime, timeframe: str) -> float:
    current_date = date
    current_date_str = current_date.strftime(DATE_FORMAT[timeframe])
    while current_date < datetime.strptime(data.index[-1], DATE_FORMAT[timeframe]):
        if current_date_str in data.index:
            return data.loc[current_date_str].Close
        else:
            current_date += get_delta(timeframe)
            current_date_str = current_date.strftime(DATE_FORMAT[timeframe])
    return data.iloc[-1].Close

def trades_2_balance_series(data, trades, timeframe, initial_balance):
    balance = initial_balance
    amount = 0
    df = []
    start = data.index[0]

    if len(trades) == 0:
        end = data.index[-1]
        df.extend(generate_range_sell(start, end, timeframe, balance))
        df = pd.DataFrame(df, columns=['date', 'balance']).drop_duplicates('date')
        return df
    for _, trade in trades.iterrows():
        # INTERVAL: UNTIL ON BUY
        df.extend(generate_range_sell(start, trade.entry_date, timeframe, balance))

        # INTERVAL: ON BUY
        price = data.loc[trade.entry_date].Close
        amount = balance / price
        balance = 0
        df.extend(generate_range_buy(data, trade.entry_date, trade.output_date, timeframe, amount))

        price = data.loc[trade.output_date].Close
        balance = amount * price
        amount = 0

        start = trade.output_date

    start = trades.iloc[-1].output_date
    end = data.index[-1]
    df.extend(generate_range_sell(start, end, timeframe, balance))

    df = pd.DataFrame(df, columns=['date', 'balance']).drop_duplicates('date')
    return df

def generate_range_sell(start, end, timeframe, balance):
    dates = generate_date_range(start, end, timeframe)
    return [{'date': date, 'balance': balance} for date in dates]

def generate_range_buy(data, start, end, timeframe, amount):
    dates = generate_date_range(start, end, timeframe)
    return [{'date': date, 'balance': amount * loc(data, datetime.strptime(date, DATE_FORMAT[timeframe]), timeframe)} for date in dates]

def buy_and_hold_balance_series(data, timeframe, initial_balance):
    amount = initial_balance / data.iloc[0].Close
    dates = generate_date_range(data.index[0], data.index[-1], timeframe)
    df = [{'date': date, 'balance': amount * loc(data, datetime.strptime(date, DATE_FORMAT[timeframe]), timeframe)} for date in dates]

    return pd.DataFrame(df, columns=['date', 'balance'])

def generate_dates(start, end):
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    dates = [start + timedelta(days=n) for n in range(int((end - start).days + 1))]
    return dates

def plot_strategy_and_buy_and_hold(data, trades, timeframe, initial_balance=1000, log_scale=False):
  df_hold = buy_and_hold_balance_series(data, timeframe, initial_balance)
  df_strategy = trades_2_balance_series(data, trades, timeframe, initial_balance)

  fig = plt.figure()
  fig.set_size_inches(30, 5)
  if log_scale:
    plt.yscale('log')

  plt.plot(generate_dates(data.index[0], data.index[-1]), df_hold.balance, color='orange')
  plt.plot(generate_dates(data.index[0], data.index[-1]), df_strategy.balance)
  plt.show()

def plot_buy_and_hold(data, initial_balance=1000, log_scale=False):
  df = buy_and_hold_balance_series(data, initial_balance)

  plot(df.index, df.balance, log_scale, color='orange')

def plot_strategy(data, trades, initial_balance=1000, log_scale=False):
  df = trades_2_balance_series(data, trades, initial_balance)
  plot(df.index, df.balance, log_scale)

def plot_df(x: pd.Series, y: pd.DataFrame, log_scale=False):
  fig = plt.figure()
  fig.set_size_inches(30, 5)
  if log_scale:
    plt.yscale('log')
  
  dates = generate_dates(x[0], x[-1])
  for column in y:
    plt.plot(dates, y[column], label = column)
  plt.legend()
  plt.show()

def plot(x: pd.Series, y: pd.Series, log_scale=False, color='#006CA7', buy_threshold=None, sell_threshold=None):
    # matplotlib works better if we set dates instead strings
    # on the axis x, the plot looks much better 
    fig = plt.figure()
    fig.set_size_inches(30, 5)

    if log_scale:
      plt.yscale('log')

    plt.plot(generate_dates(x[0], x[-1]), y, color=color)

    if buy_threshold is not None:
      plt.axhline(y=buy_threshold, color='g', linestyle='--')
    if sell_threshold is not None:
      plt.axhline(y=sell_threshold, color='r', linestyle='--')

    plt.show()
