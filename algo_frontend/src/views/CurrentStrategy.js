/* Import Libs */
import { useEffect, useState } from "react"

/* Import WebApi */
import { get } from "../webapi/strategy"

/* Import Utils */
import { capitalize } from "../utils/string"

/* Import Styles */
import { CurrentStrategyStyle } from "../styles/CurrentStrategy"

/* Import Components */
import Trades from "../components/Trades"
import View from "../components/reusables/View"
import CurrencyLogo from "../components/CurrencyLogo"

const CurrentStrategy = () => {
  const [strategy, strategyFunc] = useState({
    loading: true,
    data: {
      currencies: [],
    },
  })

  const getStrategy = () => {
    const transformToView = (data) => {
      const getDuration = (start) => {
        const currentTime = Math.floor(Date.now() / 1000)

        const durationInSeconds = currentTime - start

        const days = Math.floor(durationInSeconds / (3600 * 24))
        const hours = Math.floor((durationInSeconds % (3600 * 24)) / 3600)

        return `${days} days, ${hours} hours`
      }

      const initialBalance = data.initial_balance
      const currentBalance = parseFloat(data.current_balance).toFixed(2)
      const profitAndLoss = (currentBalance - initialBalance).toFixed(2)
      const profitAndLossPercentaje = (
        (currentBalance / initialBalance - 1) *
        100
      ).toFixed(2)
      const duration = getDuration(data.start_timestamp)

      return {
        ...data,
        current_balance: parseFloat(data.current_balance).toFixed(2),
        profit_and_loss_label: `${profitAndLoss} (${profitAndLossPercentaje}%)`,
        indicators: (data.indicators || []).map((indicator) => ({
          ...indicator,
          name: (() => {
            switch (indicator.name) {
              case "rsi":
                return "RSI"
              default:
                return capitalize(indicator.name)
            }
          })(),
          parameters: Object.keys(indicator.parameters).map((key) => ({
            key: key
              .split("_")
              .map((word) => capitalize(word))
              .join(" "),
            value: indicator.parameters[key],
          })),
        })),
        duration,
      }
    }
    get()
      .then((response) => {
        strategyFunc((prevState) => ({
          ...prevState,
          loading: false,
          data: transformToView(response.data),
        }))
      })
      .catch((_) => {})
  }

  useEffect(() => {
    getStrategy()
  }, [])

  return (
    <View
      title="Current Strategy"
      content={
        <CurrentStrategyStyle>
          <div className="summary">
            <h2>Summary</h2>
            <div className="summary-content">
              <div className="box">
                <div className="label">Initial Balance</div>
                <div className="value">{strategy.data.initial_balance}</div>
              </div>
              <div className="box">
                <div className="label">Current Balance</div>
                <div className="value">{strategy.data.current_balance}</div>
              </div>
              <div className="box">
                <div className="label">Profit/Loss</div>
                <div className="value">
                  {strategy.data.profit_and_loss_label}
                </div>
              </div>
              <div className="box">
                <div className="label">Currencies</div>
                <div className="value">
                  {strategy.data.currencies.map((currency) => (
                    <div className="currency-wrapper">
                      <CurrencyLogo currency={currency} />
                    </div>
                  ))}
                </div>
              </div>
              <div className="box">
                <div className="label">Duration</div>
                <div>{strategy.data.duration}</div>
              </div>
            </div>
          </div>
          <div className="trades">
            <h2>Trades</h2>
            <Trades strategyID={strategy.data.id} />
          </div>
        </CurrentStrategyStyle>
      }
    />
  )
}

export default CurrentStrategy
