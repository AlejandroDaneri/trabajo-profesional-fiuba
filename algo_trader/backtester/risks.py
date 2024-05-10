class RiskMetrics:
    @staticmethod
    def payoff_ratio(returns):
        losers = returns[returns < 0]
        winners = returns[returns > 0]
        if len(losers) == 0 or len(winners) == 0:
            return 0  # Retorna 0 si no hay perdedores o ganadores para evitar NaN
        payoff_ratio = abs(winners.mean() / losers.mean())
        return payoff_ratio

    @staticmethod
    def rachev_ratio(returns, alpha=0.05):
        tail_right = returns[returns > returns.quantile(1 - alpha)]
        tail_left = returns[returns < returns.quantile(alpha)]

        if tail_left.abs().mean() == 0:
            return float('inf')  # Retorna infinito si no hay datos en la cola izquierda para evitar NaN
        return round(tail_right.mean() / tail_left.abs().mean(), 3)

    @staticmethod
    def kelly_criterion(results):
        winners = results[results > 0]
        losers = results[results < 0]
        if len(winners) == 0 or len(losers) == 0 or losers.mean() == 0:
            return 0  # Retorna 0 si no hay ganadores o perdedores o si la media de perdedores es 0 para evitar NaN
        totals = len(winners) + len(losers)
        b = -winners.mean() / losers.mean()
        win_prob = len(winners) / totals
        loss_prob = 1 - win_prob
        return win_prob - loss_prob / b

    @staticmethod
    def max_drawdowns(strategy):
        drawdowns = (strategy / strategy.cummax() - 1)
        if drawdowns.min() == float('inf'):
            return 0  # Retorna 0 si hay una división por cero para evitar NaN
        return drawdowns.min()

    @staticmethod
    def profit_factor(returns):
        losers = returns[returns < 0]
        winners = returns[returns > 0]
        if losers.sum() == 0:
            return float('inf')  # Retorna infinito si la suma de pérdidas es 0 para evitar NaN
        profit_factor = -winners.sum() / losers.sum()
        return profit_factor
