/* Import Libs */
import { useEffect, useState } from "react"

/* Import WebApi */
import { list } from "../webapi/strategy"

/* Import Styles */
import StrategiesStyle from "../styles/strategies"

/* Import Utils */
import { capitalize } from "../utils/string"

/* Import Components */
import CurrencyLogo from "../components/CurrencyLogo"

const StrategiesView = () => {
  const [state, stateFunc] = useState({
    loading: false,
    data: [],
  })

  const transformToView = (data) => {
    return data.map((strategy) => ({
      ...strategy,
      state_label: capitalize(strategy.state),
    }))
  }

  useEffect(() => {
    list()
      .then((response) => {
        stateFunc({
          loading: false,
          data: transformToView(response?.data || []),
        })
      })
      .catch((_) => {
        stateFunc({
          loading: false,
        })
      })
  }, [])

  return (
    <StrategiesStyle>
      <div className="header">
        <h1>Strategies</h1>
      </div>
      <div className="content">
        <div className="strategies">
          {state.data.map((strategy) => (
            <div className="strategy">
              {strategy.state_label}
              <div className="indicators">
                {strategy.indicators.map((indicator) => (
                  <div className="indicator">{indicator.name}</div>
                ))}
              </div>
              <div className="currencies">
                {strategy.currencies.map((currency) => (
                  <div className="currency">
                    <CurrencyLogo currency={currency} />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </StrategiesStyle>
  )
}

export default StrategiesView
