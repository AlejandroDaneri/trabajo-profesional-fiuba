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

const CurrentStrategy = () => {
  const [strategy, strategyFunc] = useState({
    loading: true,
    data: {},
  })

  const getStrategy = () => {
    const transformToView = (data) => {
      const initialBalance = data.initial_balance
      const currentBalance = parseFloat(data.current_balance).toFixed(2)
      const profitAndLoss = (currentBalance - initialBalance).toFixed(2)
      const profitAndLossPercentaje = (
        (currentBalance / initialBalance - 1) *
        100
      ).toFixed(2)

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
              <div className="value">{strategy.data.profit_and_loss_label}</div>
            </div>
          </div>
          <Trades strategyID={strategy.data.id} />
        </CurrentStrategyStyle>
      }
    />
  )
}

export default CurrentStrategy
