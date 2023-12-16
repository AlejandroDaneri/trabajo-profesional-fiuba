import { useEffect, useState } from "react"
import logo from "./bitcoin.png"

/* Import Libs */
import styled from "styled-components"
import { list } from "./webapi/trade"

const AppStyle = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  background: #282c34;
  color: white;

  & img {
    height: 40vmin;
    pointer-events: none;
  }
`

const TradesStyle = styled.div`
  display: flex;
  flex-direction: column;

  & .trade {
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid white;
    justify-content: space-between;
    width: 400px;
    height: 40px;
    margin: 5px;
    border-radius: 10px;
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
          <p>{trade.pair}</p>
          <p>{trade.price}</p>
          <p>{trade.amount}</p>
        </div>
      ))}
    </TradesStyle>
  )
}

const App = () => {
  return (
    <AppStyle>
      <img src={logo} className="App-logo" alt="logo" />
      <p>SatoshiBOT.tech</p>
      <Trades />
    </AppStyle>
  )
}

export default App
