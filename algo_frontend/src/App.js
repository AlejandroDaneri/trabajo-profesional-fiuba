import { useEffect, useState } from "react"
import logo from "./bitcoin.png"

/* Import Libs */
import styled from "styled-components"
import { list } from "./webapi/trade"
import Trades from "./components/trades"

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
