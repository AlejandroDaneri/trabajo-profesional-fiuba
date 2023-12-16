/* Import Libs */
import styled from "styled-components"
import { useEffect, useState } from "react"

/* Import WebApi */
import { list } from "../webapi/trade"

/* Import Images */
import sol from "../images/logos/sol.png"
import btc from "../images/logos/btc.png"
import eth from "../images/logos/eth.png"

const TradesStyle = styled.div`
  display: flex;
  flex-direction: column;

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
    loading: false,
    data: [],
  })

  useEffect(() => {
    stateFunc((prevState) => ({
      ...prevState,
      loading: true,
    }))
    list()
      .then((response) => {
        stateFunc((prevState) => ({
          ...prevState,
          loading: false,
          data: response?.data || [],
        }))
      })
      .catch((err) => {
        stateFunc((prevState) => ({
          ...prevState,
          loading: false,
        }))
      })
  }, [])

  return (
    <TradesStyle>
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
    </TradesStyle>
  )
}

export default Trades
