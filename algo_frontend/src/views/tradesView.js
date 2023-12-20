/* Import Libs */
import { useEffect, useState } from "react"

/* Import WebApi */
import { list } from "../webapi/trade"

/* Import Images */
import btc from "../images/logos/btc.png"
import sol from "../images/logos/sol.png"
import eth from "../images/logos/eth.png"
import { unixToDate } from "../utils/date"

/* Import Styles */
import { ResultStyle, TradesStyle } from "../styles/trades"
import Topbar from "../components/topbar"
import styled from "styled-components"

const ContentStyle = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
`

const TradesView = () => {
  const [state, stateFunc] = useState({
    loading: true,
    data: [],
  })

  const transformToView = (data) => {
    return data
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
      })
  }

  useEffect(() => {
    const getState = () => {
      stateFunc((prevState) => ({
        ...prevState,
        loading: true,
      }))
      list()
        .then((response) => {
          stateFunc((prevState) => ({
            ...prevState,
            loading: false,
            data: transformToView(response?.data || []),
          }))
        })
        .catch((_) => {
          stateFunc((prevState) => ({
            ...prevState,
            loading: false,
          }))
        })
    }
    const interval = setInterval(getState, 60000)
    getState()
    return () => {
      clearInterval(interval)
    }
  }, [])

  return (
    <TradesStyle>
      {state.loading ? (
        <p>loading</p>
      ) : (
        <>
          <div className="summary">Trades executed: {state.data.length}</div>
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
            {state.data.map((trade) => (
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
