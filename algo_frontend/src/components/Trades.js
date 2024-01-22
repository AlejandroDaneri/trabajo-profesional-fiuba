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
`

const Trades = ({ strategyID }) => {
  const [state, stateFunc] = useState({
    loading: false,
    data: [],
  })

  const transformToView = (trades) => {
    return trades.map((trade) => ({
      ...trade,
      amount: parseFloat(trade.amount).toFixed(4),
      orders: {
        buy: {
          ...trade.orders.buy,
          timestamp_label: unixToDate(trade.orders.buy.timestamp),
        },
        sell: {
          ...trade.orders.sell,
          timestamp_label: unixToDate(trade.orders.sell.timestamp),
        },
      },
      duration:
        (trade.orders.sell.timestamp / 1000 -
          trade.orders.buy.timestamp / 1000) /
        60,
      pl: (
        (trade.orders.sell.price / trade.orders.buy.price - 1) *
        100
      ).toFixed(3),
    }))
  }

  useEffect(() => {
    if (strategyID) {
      list(strategyID).then((response) => {
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
    },
    {
      label: "Date Buy",
    },
    {
      label: "Date Sell",
    },
    {
      label: "Duration (min)",
    },
    {
      label: "Price Buy ($)",
    },
    {
      label: "Price Sell ($)",
    },
    {
      label: "Profit/Loss (%)",
    },
  ]

  const buildRow = (row) => {
    return [
      <CurrencyLogo currency={row.pair} />,
      row.amount,
      row.orders.buy.timestamp_label,
      row.orders.sell.timestamp_label,
      row.duration,
      row.orders.buy.price,
      row.orders.sell.price,
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
