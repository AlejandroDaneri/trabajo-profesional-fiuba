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
import { getDuration, unixToDate } from "../utils/date"

const TradesStyle = styled.div`
  display: flex;
  width: 100%;
  max-height: 600px;
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
      sell_timestamp: trade.orders.sell.timestamp,
      buy_timestamp: trade.orders.buy.timestamp,
      sell_timestamp_label: trade.orders.sell.timestamp ? unixToDate(trade.orders.sell.timestamp) : '',
      buy_timestamp_label: unixToDate(trade.orders.buy.timestamp),
      buy_price: parseFloat(trade.orders.buy.price).toFixed(2),
      sell_price: trade.orders.sell.price ? parseFloat(trade.orders.sell.price).toFixed(2) : '',
      duration:  getDuration(trade.orders.buy.timestamp, trade.orders.sell.timestamp),
      pl: trade.orders.sell.timestamp ? ((trade.orders.sell.price / trade.orders.buy.price - 1) * 100).toFixed(3) : '',
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
      sortable: true,
    },
    {
      value: "buy_timestamp",
      label: "Date Buy",
      sortable: true,
      default: true,
      direction: 'desc',
    },
    {
      value: "sell_timestamp",
      label: "Date Sell",
      sortable: true,
    },
    {
      value: "duration",
      label: "Duration",
      sortable: true,
    },
    {
      value: "buy_price",
      label: "Price Buy ($)",
      sortable: true,
    },
    {
      value: "sell_price",
      label: "Price Sell ($)",
      sortable: true,
    },
    {
      value: "pl",
      label: "Profit/Loss (%)",
      sortable: true,
    },
  ]

  const buildRow = (row) => {
    return [
      <CurrencyLogo currency={row.pair} />,
      row.amount,
      row.buy_timestamp_label,
      row.sell_timestamp_label,
      row.duration,
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
