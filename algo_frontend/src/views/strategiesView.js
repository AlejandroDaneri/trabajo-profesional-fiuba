/* Import Libs */
import { useEffect, useState } from "react"

/* Import WebApi */
import { list, stop } from "../webapi/strategy"

/* Import Styles */
import StrategiesStyle from "../styles/strategies"

/* Import Utils */
import { capitalize } from "../utils/string"

/* Import Components */
import CurrencyLogo from "../components/CurrencyLogo"
import Table from "../components/Table"
import Button from "../components/Button"

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

  const list_ = () => {
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
  }

  useEffect(() => {
    list_()
  }, []) // eslint-disable-line

  const headers = [
    {
      value: "state",
      label: "State",
    },
    {
      value: "initial_balance",
      label: "Initial Balance",
    },
    {
      value: "indicators",
      label: "Indicators",
    },
    {
      value: "currencies",
      label: "Currencies",
    },
    {
      value: "actions",
      label: "Actions",
    },
  ]

  const onStopStrategy = (strategyId) => {
    stop(strategyId)
      .then((_) => {
        list_()
      })
      .catch((_) => {})
  }

  const onShowTrades = () => {}

  const buildRow = (row) => {
    return [
      capitalize(row.state),
      row.initial_balance,
      <div className="indicators">
        {row.indicators.map((indicator) => (
          <div className="indicator">{indicator.name}</div>
        ))}
      </div>,
      <div className="currencies">
        {row.currencies.map((currency) => (
          <div className="currency">
            <CurrencyLogo currency={currency} />
          </div>
        ))}
      </div>,
      <div className="actions">
        {row.state === "running" && (
          <Button text="Stop" onClick={() => onStopStrategy(row.id)} />
        )}
        <Button text="Trades" onClick={() => onShowTrades(row.id)} />
      </div>,
    ]
  }

  return (
    <StrategiesStyle>
      <div className="header">
        <h1>Strategies</h1>
      </div>
      <div className="content">
        <div className="strategies">
          <Table headers={headers} data={state.data} buildRow={buildRow} />
        </div>
      </div>
    </StrategiesStyle>
  )
}

export default StrategiesView
