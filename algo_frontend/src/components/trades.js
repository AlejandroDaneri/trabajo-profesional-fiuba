/* Import Libs */
import styled from "styled-components"
import { useEffect, useState } from "react"

/* Import WebApi */
import { list } from "../webapi/trade"

/* Import Images */
import btc from "../images/logos/btc.png"

const TradesStyle = styled.div`
  display: flex;
  flex-direction: column;
  height: 600px;

  & p {
    color: white;
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
    width: 400px;
    height: 40px;
    margin: 5px;
    border-radius: 10px;
    padding-left: 10px;
    padding-right: 10px;

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
    }

    & .amount {
    }
  }
`
const Trades = () => {
  const [state, stateFunc] = useState({
    loading: true,
    data: [],
  })

  const getState = () => {
    console.info("hola")
    stateFunc((prevState) => ({
      ...prevState,
      loading: true,
    }))
    list()
      .then((response) => {
        console.info("ok")
        stateFunc((prevState) => ({
          ...prevState,
          loading: false,
          data: response?.data || [],
        }))
      })
      .catch((err) => {
        console.info("err")
        stateFunc((prevState) => ({
          ...prevState,
          loading: false,
        }))
      })
  }

  useEffect(() => {
    const interval = setInterval(getState, 60000)
    return () => {
      clearInterval(interval)
    }
  }, [])

  return (
    <TradesStyle>
      {state.loading ? (
        <p>loading</p>
      ) : (
        <div className="trades">
          {state.data.map((trade) => (
            <div className="trade">
              <div className="coin">
                <img src={btc} alt="logo" />
                <p>{trade.pair}</p>
              </div>
              <div className="price">${trade.price}</div>
              <div className="amount">{trade.amount}</div>
            </div>
          ))}
        </div>
      )}
    </TradesStyle>
  )
}

export default Trades
