def calculate_payoff_ratio(returns):
    losers = returns[returns<0]
    winners = returns[returns>0]
    payoff_ratio = abs(winners.mean() / losers.mean())
    return payoff_ratio

def calculate_rachev_ratio(returns,alpha =0.05):
    tail_right = returns[returns > returns.quantile(1-alpha)]
    tail_left = returns[returns > returns.quantile(alpha)]

    return round(tail_right.mean() / tail_left.abs().mean(),3)

def calculate_kelly_criterion(results):
    winners = results[results>0]
    losers = results[results<0]
    totals = len(winners) + len(losers)
    b = -winners.mean() / losers.mean()
    win_prob = len(winners)/ totals
    loss_prob = 1 - win_prob
    return win_prob - loss_prob / b

def calculate_max_drawdowns(strategy):
    drawdowns = (strategy / strategy.cummax() - 1)
    return drawdowns.min()

def calculate_profit_factor(returns):
    losers = returns[returns<0]
    winners = returns[returns>0]
    profit_factor = - winners.sum()/losers.sum()
    return profit_factor