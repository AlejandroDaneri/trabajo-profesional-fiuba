import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def expand_trades(data, trades, initial_balance):
    def generate_range_sell(start, end, balance):
      df = pd.DataFrame(columns=['balance'])

      start_date = datetime.strptime(start, '%Y-%m-%d')
      end_date = datetime.strptime(end, '%Y-%m-%d')

      for n in range(int((end_date - start_date).days + 1)):
        current = (start_date + timedelta(days=n)).strftime('%Y-%m-%d')
        df.loc[current] = {
          'balance': balance
        }

      return df

    def generate_range_buy(start, end, amount):
      df = pd.DataFrame(columns=['balance'])

      start_date = datetime.strptime(start, '%Y-%m-%d')
      end_date = datetime.strptime(end, '%Y-%m-%d')

      for n in range(int((end_date - start_date).days + 1)):
        current = (start_date + timedelta(days=n)).strftime('%Y-%m-%d')
        df.loc[current] = {
          'balance': amount * data.loc[current].Close
        }

      return df

    df = pd.DataFrame(columns=['balance'])
    balance = initial_balance
    amount = 0
    start = data.index[0]

    for index, trade in trades.iterrows():
      trade = trades.iloc[index]

      # INTERVAL: UNTIL ON BUY
      df_until_buy = generate_range_sell(start, trade.buy_date, balance)
      df = pd.concat([df, df_until_buy])

      # INTERVAL: ON BUY
      price = data.loc[trade.buy_date].Close
      amount = balance / price
      balance = 0
      df_interval_buy = generate_range_buy(trade.buy_date, trade.sell_date, amount)
      df = pd.concat([df, df_interval_buy])

      price = data.loc[trade.sell_date].Close
      balance = amount * price
      amount = 0
      
      start = trade.sell_date
  
    start = trades.iloc[-1].sell_date
    end = data.index[-1]
    df_final_interval = generate_range_sell(start, end, balance)
    df = pd.concat([df, df_final_interval])
    df = df[~df.index.duplicated(keep='first')]

    return df

def generate_dataframe_buy_and_hold(data, initial_balance):
  amount = initial_balance / data.iloc[0].Close

  df = pd.DataFrame(columns=['balance'])

  start = data.index[0]
  end = data.index[-1]

  start_date = datetime.strptime(start, '%Y-%m-%d')
  end_date = datetime.strptime(end, '%Y-%m-%d')

  for n in range(int((end_date - start_date).days + 1)):
    current = (start_date + timedelta(days=n)).strftime('%Y-%m-%d')
    df.loc[current] = {
      'balance': amount * data.loc[current].Close
    }

  return df

def generate_dates(start, end):
  start = datetime.strptime(start, '%Y-%m-%d')
  end = datetime.strptime(end, '%Y-%m-%d')
  dates = []
  for n in range(int((end - start).days + 1)):
    dates.append(start + timedelta(days=n))
  return dates

def plot_strategy_and_buy_and_hold(data, trades, initial_balance=1000, log_scale=False):
  df_hold = generate_dataframe_buy_and_hold(data, initial_balance)
  df_strategy = expand_trades(data, trades, initial_balance)

  fig = plt.figure()
  fig.set_size_inches(30, 5)
  if log_scale:
    plt.yscale('log')

  plt.plot(generate_dates(data.index[0], data.index[-1]), df_hold.balance, color='orange')
  plt.plot(generate_dates(data.index[0], data.index[-1]), df_strategy.balance)
  plt.show()

def plot_buy_and_hold(data, initial_balance=1000, log_scale=False):
  df = generate_dataframe_buy_and_hold(data, initial_balance)

  plot(df.index, df.balance, log_scale, color='orange')

def plot_strategy(data, trades, initial_balance=1000, log_scale=False):
  df = expand_trades(data, trades, initial_balance)
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
