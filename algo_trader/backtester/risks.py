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

def calculate_kelly_criterion(results):
    winners = results[results>0]
    losers = results[results<0]
    totals = len(winners) + len(losers)
    b = -winners.mean() / losers.mean()
    win_prob = len(winners)/ totals
    loss_prob = 1 - win_prob
    return win_prob - loss_prob / b

def calculate_drawdowns(trades):
    cumulative_return = trades["cumulative_return"]
    previous_peaks = cumulative_return.cummax()
    drawdowns = cumulative_return - previous_peaks
    return drawdowns

def calculate_profit_factor(returns):
    losers = returns[returns<0]
    winners = returns[returns>0]
    profit_factor = - winners.sum()/losers.sum()
    return profit_factor