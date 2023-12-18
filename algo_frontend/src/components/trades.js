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
import { TradesStyle, TypeStyle } from "../styles/trades"

const Trades = () => {
  const [state, stateFunc] = useState({
    loading: true,
    data: [],
  })

  const transformToView = (data) => {
    return data
      .map((row) => {
        return {
          ...row,
          timestamp_label: unixToDate(row.timestamp),
        }
      })
      .sort((a, b) => {
        if (a.timestamp < b.timestamp) {
          return 1
        } else if (a.timestamp > b.timestamp) {
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
            {state.data.map((trade) => (
              <div className="trade">
                <div className="timestamp">{trade.timestamp_label}</div>
                <TypeStyle type={trade.type}>{trade.type}</TypeStyle>
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
                  <p>{trade.pair}</p>
                </div>
                <div className="price">${trade.price}</div>
                <div className="amount">{trade.amount}</div>
              </div>
            ))}
          </div>
        </>
      )}
    </TradesStyle>
  )
}

export default Trades
