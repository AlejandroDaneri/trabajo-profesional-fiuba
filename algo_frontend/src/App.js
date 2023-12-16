/* Import Libs */
import styled from "styled-components"

/* Import Components */
import Trades from "./components/trades"

/* Import Images */
import logo from "./images/bitcoin.png"

const AppStyle = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  background: #282c34;
  color: white;

  & .logo {
    display: flex;
    align-items: center;
    justify-content: space-around;
    border: 1px solid white;
    border-radius: 10px;
    width: 260px;
    height: 120px;
    margin: 20px;
    box-shadow: white 0px 2px 8px 0px;

    & img {
      height: 96px;
      height: 96px
      pointer-events: none;
    }

    & p {
      font-weight: 600;
    }
  }
`

const App = () => {
  return (
    <AppStyle>
      <div className="logo">
        <img src={logo} className="App-logo" alt="logo" />
        <p>SatoshiBOT.tech</p>
      </div>
      <Trades />
    </AppStyle>
  )
}

export default App
