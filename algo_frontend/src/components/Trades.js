/* Import Libs */
import { useEffect, useState } from "react"
import styled from "styled-components"

/* Import WebApi */
import { list } from "../webapi/trade"

/* Import Components */
import CurrencyLogo from "./CurrencyLogo"
import Table from "./Table"

/* Import Styles */
import { ResultStyle } from "../styles/CurrentStrategy"

/* Import Utils */
import { unixToDate } from "../utils/date"

const TradesStyle = styled.div`
  display: flex;
  width: 100%;
`

const Trades = ({ strategyID }) => {
  const [state, stateFunc] = useState({
    loading: false,
    data: [],
  })

  const transformToView = (trades) => {
    return trades.map((trade) => {

      if (trade.id === 'current') {
        return {
          pair: trade.pair,
          amount: parseFloat(trade.amount).toFixed(4),
          buy_timestamp: trade.orders.buy.timestamp,
          buy_timestamp_label: unixToDate(trade.orders.buy.timestamp),
        }
      } else {
        return {
          ...trade,
          amount: parseFloat(trade.amount).toFixed(4),
          sell_timestamp: trade.orders.sell.timestamp,
          buy_timestamp: trade.orders.buy.timestamp,
          sell_timestamp_label: unixToDate(trade.orders.sell.timestamp),
          buy_timestamp_label: unixToDate(trade.orders.buy.timestamp),
          buy_price: trade.orders.buy.price,
          sell_price: trade.orders.sell.price,
          duration: (trade.orders.sell.timestamp / 1000 - trade.orders.buy.timestamp / 1000) / 60,
          pl: ((trade.orders.sell.price / trade.orders.buy.price - 1) * 100).toFixed(3),
        }
      }
    })
  }

  useEffect(() => {
    if (strategyID) {
      list(strategyID)
        .then((response) => {
          stateFunc((prevState) => ({
            ...prevState,
            data: transformToView(response.data),
          }))
        })
    }
  }, [strategyID])

  const headers = [
    {
      value: "coin",
      label: "Coin",
    },
    {
      value: "amount",
      label: "Amount",
      sortable: true
    },
    {
      value: "buy_timestamp",
      label: "Date Buy",
      sortable: true,
      default: true
    },
    {
      value: "sell_timestamp",
      label: "Date Sell",
      sortable: true
    },
    {
      value: 'duration',
      label: "Duration (min)",
      sortable: true
    },
    {
      value: "buy_price",
      label: "Price Buy ($)",
      sortable: true
    },
    {
      value: "sell_price",
      label: "Price Sell ($)",
      sortable: true
    },
    {
      value: "pl",
      label: "Profit/Loss (%)",
      sortable: true
    },
  ]

  const buildRow = (row) => {
    return [
      <CurrencyLogo currency={row.pair} />,
      row.amount,
      row.buy_timestamp_label,
      row.sell_timestamp_label,
      row.duration.toFixed(4),
      row.buy_price,
      row.sell_price,
      <ResultStyle win={row.pl > 0}>{row.pl} </ResultStyle>,
    ]
  }

  return (
    <TradesStyle>
      {state.loading ? (
        "loading"
      ) : (
        <Table headers={headers} data={state.data} buildRow={buildRow} />
      )}
    </TradesStyle>
  )
}

export default Trades
