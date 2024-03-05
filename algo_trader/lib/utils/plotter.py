import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot(x: pd.Series, y: pd.Series, log_scale=False):
    # matplotlib works better if we set dates instead strings
    # on the axis x, the plot looks much better 
    start = datetime.strptime(x[0], '%Y-%m-%d')
    end = datetime.strptime(x[-1], '%Y-%m-%d')
    dates = []
    for n in range(int((end - start).days + 1)):
        dates.append(start + timedelta(days=n))

    fig = plt.figure()
    fig.set_size_inches(30, 5)
    if log_scale:
      plt.yscale('log')
    plt.plot(dates, y)
    plt.show()
