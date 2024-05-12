import numpy as np
class RiskMetrics:
    @staticmethod
    def payoff_ratio(returns):
        losers = returns[returns < 0]
        winners = returns[returns > 0]
        if len(losers) == 0 or len(winners) == 0:
            return 0  
        payoff_ratio = abs(winners.mean() / losers.mean())
        return payoff_ratio

    @staticmethod
    def rachev_ratio(returns, alpha=0.05):
        tail_right = returns[returns > returns.quantile(1 - alpha)]
        tail_left = returns[returns < returns.quantile(alpha)]
        if(len(tail_left.array) == 0 or len(tail_right.array)== 0):
            return 0
        
        if tail_left.abs().mean() == 0:
            return 99999999
        return round(tail_right.mean() / tail_left.abs().mean(), 3)

    @staticmethod
    def kelly_criterion(results):
        winners = results[results > 0]
        losers = results[results < 0]
        if len(winners) == 0 or len(losers) == 0 or losers.mean() == 0:
            return 0 
        totals = len(winners) + len(losers)
        b = -winners.mean() / losers.mean()
        win_prob = len(winners) / totals
        loss_prob = 1 - win_prob
        return win_prob - loss_prob / b

    @staticmethod
    def max_drawdowns(strategy):
        drawdowns = (strategy / strategy.cummax() - 1)
        if drawdowns.min() == float('inf'):
            return 0  
        if drawdowns.min() == -float('inf'):
            return -99999999  
        result = drawdowns.min()
        return 0 if np.isnan(result) else result

    @staticmethod
    def profit_factor(returns):
        if len(returns) == 0:
            return 1

        losers = returns[returns < 0]
        winners = returns[returns > 0]

        if len(losers) == 0: 
            return 999999

        profit_factor = - winners.sum() / losers.sum()
        return profit_factor
