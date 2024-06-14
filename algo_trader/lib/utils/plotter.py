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

def trades_2_balance_series(data: pd.DataFrame, trades: pd.DataFrame, timeframe: str, initial_balance: int):
    df = []
    start = data.index[0]

    if len(trades) == 0:
        end = data.index[-1]
        df.extend(generate_range_sell(start, end, timeframe))
        df = pd.DataFrame(df, columns=['date', 'return']).drop_duplicates('date')
        return df
    for _, trade in trades.iterrows():
        # INTERVAL: UNTIL ON BUY
        df.extend(generate_range_sell(start, trade.entry_date, timeframe))

        # INTERVAL: ON BUY
        df.extend(generate_range_buy(data, trade.entry_date, trade.output_date, timeframe, trade.get("position_type", default="long")))
        start = trade.output_date

    start = trades.iloc[-1].output_date
    end = data.index[-1]
    df.extend(generate_range_sell(start, end, timeframe))
    df = pd.DataFrame(df, columns=['date', 'return', 'balance']).drop_duplicates('date')
    cumulative_return = (1 + df["return"]).cumprod() - 1
    df["cumulative_return"] = cumulative_return
    df["balance"] = (df['cumulative_return'] + 1) * initial_balance
    return df

def generate_range_sell(start, end, timeframe):
    dates = generate_date_range(start, end, timeframe)
    return [{'date': date, 'return': 0} for date in dates]

def generate_range_buy(data, start, end, timeframe, type = 'long'):
  dates = generate_date_range(start, end, timeframe)

  def get_return(date):
    now_price = loc(data, datetime.strptime(date, DATE_FORMAT[timeframe]), timeframe)
    prev_price = loc(data, datetime.strptime(date, DATE_FORMAT[timeframe]) - get_delta(timeframe), timeframe)

    if type == 'long':
      return now_price / prev_price - 1
    else:
      return prev_price / now_price - 1
        
  return_ = []
  for date in dates:
    return_.append({'date': date, 'return': get_return(date)})
  return return_

def buy_and_hold_balance_series(data, timeframe, initial_balance):
    list = generate_range_buy(data, data.index[0], data.index[-1], timeframe)
    df = pd.DataFrame(list, columns=['date', 'return']).drop_duplicates('date')
    cumulative_return = (1 + df["return"]).cumprod() - 1
    df["cumulative_return"] = cumulative_return
    df["balance"] = (df['cumulative_return'] + 1) * initial_balance
    return df

def generate_dates(start: str, end: str):
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

def plot_buy_and_hold(data, initial_balance=1000, timeframe='1d', log_scale=False):
  df = buy_and_hold_balance_series(data, timeframe, initial_balance)
  plot(df.date, df.balance, log_scale, color='orange')

def plot_strategy(data, trades, initial_balance=1000, log_scale=False, timeframe='1d'):
  df = trades_2_balance_series(data, trades, timeframe, initial_balance)
  plot(df.date, df.balance, log_scale)

def plot_df(x: pd.Series, y: pd.DataFrame, log_scale=False):
  fig = plt.figure()
  fig.set_size_inches(30, 10)
  if log_scale:
    plt.yscale('log')
  
  dates = generate_dates(x[0], x[-1])
  for column in y:
    plt.plot(dates, y[column], label = column)
  plt.xticks(fontsize=16)
  plt.yticks(fontsize=16) 
  plt.legend(fontsize=14)
  plt.ylabel('Percentage', fontsize=14)
  plt.show()

def plot(x: pd.Series, y: pd.Series, log_scale=False, color='#006CA7', buy_threshold=None, sell_threshold=None):
    # matplotlib works better if we set dates instead strings
    # on the axis x, the plot looks much better 
    fig = plt.figure()
    fig.set_size_inches(30, 5)

    if log_scale:
      plt.yscale('log')

    plt.plot(generate_dates(x.iloc[0], x.iloc[-1]), y, color=color)

    if buy_threshold is not None:
      plt.axhline(y=buy_threshold, color='g', linestyle='--')
    if sell_threshold is not None:
      plt.axhline(y=sell_threshold, color='r', linestyle='--')

    plt.show()
