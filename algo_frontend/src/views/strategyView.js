/* Import Libs */
import React, { useState } from "react"
import { useEffect } from "react"

/* Import Styles */
import StrategyStyle from "../styles/strategy"

/* Import WebApi */
import { getStrategy } from "../webapi/strategy"

/* Import Images */
import btc from "../images/logos/btc.png"
import sol from "../images/logos/sol.png"
import eth from "../images/logos/eth.png"
import { capitalize } from "../utils/string"

const StrategyView = () => {
  const [state, stateFunc] = useState({
    loading: true,
    data: {
      currencies: [],
      indicators: [],
    },
  })

  const transformToView = (data) => {
    return {
      ...data,
      indicators: data.indicators.map((indicator) => ({
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

  useEffect(() => {
    stateFunc((prevState) => ({
      ...prevState,
      loading: true,
    }))
    getStrategy()
      .then((response) => {
        stateFunc((prevState) => ({
          ...prevState,
          loading: false,
          data: transformToView(response.data),
        }))
      })
      .catch((_) => {})
  }, [])

  return (
    <StrategyStyle>
      <div className="currencies">
        {state.data.currencies.map((currency) => (
          <div className="coin">
            {(() => {
              switch (currency) {
                case "BTC":
                  return <img src={btc} alt="logo" />
                case "SOL":
                  return <img src={sol} alt="logo" />
                case "ETH":
                  return <img src={eth} alt="logo" />
                default:
                  return <></>
              }
            })()}
            <p>{currency}</p>
          </div>
        ))}
      </div>
      <div className="indicators">
        {state.data.indicators.map((indicator) => (
          <div className="indicator">
            <div className="name">{capitalize(indicator.name)}</div>
            <div className="parameters">
              {indicator.parameters.map((parameter) => (
                <div className="parameter">
                  <>{parameter.key}: </>
                  <>{parameter.value}</>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </StrategyStyle>
  )
}

export default StrategyView
