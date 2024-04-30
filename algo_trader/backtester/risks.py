def calculate_payoff_ratio(trades):
    winners = trades[trades["result"] == "Winner"]["return"]
    losers = trades[trades["result"] == "Loser"]["return"]
    payoff_ratio = abs(winners.mean() / losers.mean())
    return payoff_ratio

def calculate_rachev_ratio(trades):
    mean_return = trades["return"].mean()
    downside_deviation = trades[trades["return"] < mean_return]["return"].std()
    rachev_ratio = mean_return / downside_deviation
    return rachev_ratio

def calculate_kelly_criterion(trades):
    win_rate = (trades["result"] == "Winner").mean()
    average_win = trades[trades["result"] == "Winner"]["return"].mean()
    average_loss = trades[trades["result"] == "Loser"]["return"].mean()
    kelly_fraction = (win_rate * (average_win / abs(average_loss))) - (1 - win_rate)
    return kelly_fraction

def calculate_drawdowns(trades):
    cumulative_return = trades["cumulative_return"]
    previous_peaks = cumulative_return.cummax()
    drawdowns = cumulative_return - previous_peaks
    return drawdowns

def calculate_profit_factor(trades):
    winners = trades[trades["result"] == "Winner"]["return"].sum()
    losers = trades[trades["result"] == "Loser"]["return"].sum()
    profit_factor = abs(winners / losers)
    return profit_factor
