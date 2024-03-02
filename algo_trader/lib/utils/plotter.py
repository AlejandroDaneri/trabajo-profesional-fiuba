import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    fig = plt.figure()
    fig.set_size_inches(30, 5)
    plt.plot(data.index, data.Close)
    plt.show()
