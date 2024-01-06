/* Import Libs */
import { useEffect, useState } from "react"

/* Import WebApi */
import { list } from "../webapi/trade"
import { get } from "../webapi/strategy"

/* Import Images */
import btc from "../images/logos/btc.png"
import sol from "../images/logos/sol.png"
import eth from "../images/logos/eth.png"

/* Import Utils */
import { unixToDate } from "../utils/date"
import { capitalize } from "../utils/string"

/* Import Styles */
import { ResultStyle, TradesStyle } from "../styles/trades"

const TradesView = () => {
  const [trades, tradesFunc] = useState({
    loading: true,
    data: {
      list: [],
      summary: {},
    },
  })

  const [strategy, strategyFunc] = useState({
    loading: true,
    data: {},
  })

  useEffect(() => {
    const getTrades = () => {
      const transformToView = (data) => {
        let data_ = {
          summary: {},
          list: data
            .map((row) => {
              return {
                ...row,
                amount: parseFloat(row.amount).toFixed(4),
                orders: {
                  buy: {
                    ...row.orders.buy,
                    timestamp_label: unixToDate(row.orders.buy.timestamp),
                  },
                  sell: {
                    ...row.orders.sell,
                    timestamp_label: unixToDate(row.orders.sell.timestamp),
                  },
                },
                duration:
                  (row.orders.sell.timestamp / 1000 -
                    row.orders.buy.timestamp / 1000) /
                  60,
                pl: (
                  (row.orders.sell.price / row.orders.buy.price - 1) *
                  100
                ).toFixed(3),
              }
            })
            .sort((a, b) => {
              if (a.orders.buy.timestamp < b.orders.buy.timestamp) {
                return 1
              } else if (a.orders.buy.timestamp > b.orders.buy.timestamp) {
                return -1
              } else {
                return 0
              }
            }),
        }

        data_.summary.n = data_.list.length
        data_.summary.n_profit = data_.list.filter((row) => row.pl > 0).length
        data_.summary.n_loss = data_.list.filter((row) => row.pl < 0).length

        return data_
      }
      tradesFunc((prevState) => ({
        ...prevState,
        loading: true,
      }))
      list()
        .then((response) => {
          tradesFunc((prevState) => ({
            ...prevState,
            loading: false,
            data: transformToView(response?.data || []),
          }))
        })
        .catch((_) => {
          tradesFunc((prevState) => ({
            ...prevState,
            loading: false,
          }))
        })
    }
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
    const interval = setInterval(getTrades, 60000)
    getTrades()
    getStrategy()
    return () => {
      clearInterval(interval)
    }
  }, [])

  return (
    <TradesStyle>
      {trades.loading ? (
        <p>loading</p>
      ) : (
        <>
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
            <div className="box">
              <div className="label">Trades executed</div>
              <div className="value">{trades.data.summary.n}</div>
            </div>
            <div className="box">
              <div className="label">Trades profit</div>
              <div className="value">{trades.data.summary.n_profit}</div>
            </div>
            <div className="box">
              <div className="label">Trades loss</div>
              <div className="value">{trades.data.summary.n_loss}</div>
            </div>
          </div>
          <div className="trades">
            <div className="row">
              <div className="column">Coin</div>
              <div className="column">Amount</div>
              <div className="column">Date Buy</div>
              <div className="column">Date Sell</div>
              <div className="column">Duration (min)</div>
              <div className="column">Price Buy ($)</div>
              <div className="column">Price Sell ($)</div>
              <div className="column">Profit/Loss (%)</div>
            </div>
            {trades.data.list.map((trade) => (
              <div className="row">
                <div className="column">
                  <div className="coin">
                    {(() => {
                      switch (trade.pair) {
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
                  </div>
                  <p>{trade.pair}</p>
                </div>
                <div className="column">{trade.amount}</div>
                <div className="column">{trade.orders.buy.timestamp_label}</div>
                <div className="column">
                  {trade.orders.sell.timestamp_label}
                </div>
                <div className="column">{trade.duration}</div>
                <div className="column">{trade.orders.buy.price}</div>
                <div className="column">{trade.orders.sell.price}</div>
                <div className="column">
                  <ResultStyle win={trade.pl > 0}>{trade.pl} </ResultStyle>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </TradesStyle>
  )
}

export default TradesView
