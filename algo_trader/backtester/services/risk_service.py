import numpy as np
import pandas as pd

class RiskCalculator:
    def __init__(self, returns: pd.Series, linear_returns: pd.Series):
        self.returns = returns
        self.linear_returns = linear_returns

    def payoff_ratio(self) -> float:
        losers = self.linear_returns[self.linear_returns < 0]
        winners = self.linear_returns[self.linear_returns > 0]
        if len(losers) == 0 or len(winners) == 0:
            return 0  
        return abs(winners.mean() / losers.mean())

    def rachev_ratio(self, alpha: float = 0.05) -> float:
        tail_right = self.returns[self.returns > self.returns.quantile(1 - alpha)]
        tail_left = self.returns[self.returns < self.returns.quantile(alpha)]
        if len(tail_left.array) == 0 or len(tail_right.array) == 0:
            return 0
        if tail_left.abs().mean() == 0:
            return 99999999
        return round(tail_right.mean() / tail_left.abs().mean(), 3)

    def kelly_criterion(self) -> float:
        winners = self.returns[self.returns > 0]
        losers = self.returns[self.returns < 0]
        if len(winners) == 0 or len(losers) == 0 or losers.mean() == 0:
            return 0 
        totals = len(winners) + len(losers)
        b = -winners.mean() / losers.mean()
        win_prob = len(winners) / totals
        loss_prob = 1 - win_prob
        return win_prob - loss_prob / b

    def max_drawdowns(self) -> float:
        drawdowns = (self.linear_returns / self.linear_returns.cummax() - 1)
        if drawdowns.min() == float('inf'):
            return 100  
        if drawdowns.min() == -float('inf'):
            return -100
        result = drawdowns.min()
        return 0 if np.isnan(result) else result

    def profit_factor(self) -> float:
        if len(self.returns) == 0:
            return 1

        losers = self.returns[self.returns < 0]
        winners = self.returns[self.returns > 0]

        if len(losers) == 0: 
            return 999999

        return -winners.sum() / losers.sum()

    def sortino_ratio(self, risk_free_rate: float = 0) -> float:
        downside_returns = self.returns[self.returns < risk_free_rate]
        expected_return = self.returns.mean() - risk_free_rate
        downside_std = downside_returns.std()
        if downside_std == 0:
            return float('inf')
        return expected_return / downside_std

    def sharpe_ratio(self, risk_free_rate: float = 0) -> float:
        excess_return = self.returns.mean() - risk_free_rate
        std_dev = self.returns.std()
        if std_dev == 0:
            return float('inf')
        return excess_return / std_dev

    def volatility(self) -> float:
        return self.returns.std()

    def value_at_risk(self, alpha: float = 0.05) -> float:
        return self.returns.quantile(alpha)

    def conditional_value_at_risk(self, alpha: float = 0.05) -> float:
        var = self.value_at_risk(alpha)
        tail_losses = self.returns[self.returns <= var]
        return tail_losses.mean()

    def calculate(self) -> dict:
        return {
            "payoff_ratio": self.payoff_ratio(),
            "rachev_ratio": self.rachev_ratio(),
            "kelly_criterion": self.kelly_criterion(),
            "max_drawdown": self.max_drawdowns(),
            "profit_factor": self.profit_factor(),
            "sortino_ratio": self.sortino_ratio(),
            "sharpe_ratio": self.sharpe_ratio(),
            "volatility": self.volatility(),
            "value_at_risk": self.value_at_risk(),
            "conditional_value_at_risk": self.conditional_value_at_risk(),
        }
