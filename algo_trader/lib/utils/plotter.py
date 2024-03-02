import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot(data: pd.DataFrame, log_scale=False):
    # matplotlib works better if we set dates instead strings
    # on the axis x, the plot looks much better 
    start = datetime.strptime(data.iloc[0].Date, '%d-%m-%Y')
    end = datetime.strptime(data.iloc[-1].Date, '%d-%m-%Y')
    dates = []
    for n in range(int((end - start).days + 1)):
        dates.append(start + timedelta(days=n))

    fig = plt.figure()
    fig.set_size_inches(30, 5)
    if log_scale:
      plt.yscale('log')
    plt.plot(dates, data.Close)
    plt.show()
