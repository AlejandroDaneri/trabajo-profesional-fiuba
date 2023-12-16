/* Import Libs */
import styled from "styled-components"
import { useEffect, useState } from "react"

/* Import WebApi */
import { list } from "../webapi/trade"

/* Import Images */
import btc from "../images/logos/btc.png"
import { unixToDate } from "../utils/date"

const TradesStyle = styled.div`
  display: flex;
  flex-direction: column;
  height: 600px;

  & p {
    color: white;
  }

  .trades::-webkit-scrollbar {
    width: 5px;
  }

  .trades::-webkit-scrollbar-track {
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  }

  .trades::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }

  & .trades {
    overflow-y: scroll;
  }

  & .trade {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    border: 1px solid white;
    width: 700px;
    height: 40px;
    margin: 5px;
    border-radius: 10px;
    padding-left: 10px;
    padding-right: 10px;

    & .timestamp {
      width: 160px;
    }

    & .coin {
      display: flex;
      align-items: center;
      width: 60px;
      justify-content: space-around;

      & img {
        width: 24px;
        height: 24px;
      }
    }

    & .price {
      width: 60px;
    }

    & .amount {
      width: 200px;
    }
  }
`
const Trades = () => {
  const [state, stateFunc] = useState({
    loading: true,
    data: [],
  })

  const transformToView = (data) => {
    return data.map((row) => {
      return {
        ...row,
        timestamp_label: unixToDate(row.timestamp),
      }
    })
  }

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

  useEffect(() => {
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
                <div className="coin">
                  <img src={btc} alt="logo" />
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
