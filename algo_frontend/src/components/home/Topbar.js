/* Import Libs */
import styled from "styled-components"
import { useHistory } from "react-router-dom"
import { useRecoilState } from "recoil"
import { useLocation } from "react-router-dom"
import { useEffect, useState } from "react"

/* Import Styles */
import TopbarStyle from "../../styles/topbar"

/* Import Images */
import logo from "../../images/bitcoin.png"

/* Import WebApi */
import { getRunning } from "../../webapi/strategy"

import { userState } from "../../atoms/atoms"
import { theme } from "../../utils/theme"

const ButtonMenuStyle = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${({ selected }) => (selected ? theme.btc : theme.dark)};
  border: none;
  cursor: pointer;
  transition: color 0.3s;
  height: 100%;
  width: 200px;
  transition: background-color 1s ease;

  & i {
    margin-right: 10px;
    font-size: 22px;
    padding: 0;
    color: ${({ selected }) => (selected ? "#000000" : theme.white)};
  }

  & p {
    font-size: 14px;
    font-weight: 600;
    color: ${({ selected }) => (selected ? "#000000" : theme.white)};
  }
`

const ButtonMenu = ({ route, title, icon }) => {
  const history = useHistory()
  const location = useLocation()
  return (
    <ButtonMenuStyle
      onClick={() => history.push(route)}
      selected={location.pathname === route}
    >
      {icon && <i className="material-icons">{icon}</i>}
      <p>{title}</p>
    </ButtonMenuStyle>
  )
}

const Topbar = () => {
  const history = useHistory()

  const [runningStrategy, runningStrategyFunc] = useState(false)

  // eslint-disable-next-line
  const [user, setUser] = useRecoilState(userState)

  const onLogout = () => {
    setUser({
      user: {},
      isLoggedIn: false,
    })
    history.push("/")
  }

  useEffect(() => {
    const getRunningStrategy = () => {
      getRunning()
        .then(_ => {
          runningStrategyFunc(true)
        })
        .catch(_ => {
          runningStrategyFunc(false)
        })
    }

    const interval = setInterval(getRunningStrategy, 5000)
    getRunningStrategy()

    return () => {
      clearInterval(interval)
    }
    
  }, [])

  return (
    <TopbarStyle>
      <div className="logo">
        <img src={logo} className="App-logo" alt="logo" />
        <p>SatoshiBOT</p>
      </div>
      <div className="nav-links">
        {runningStrategy && <ButtonMenu
          route="/home/trades"
          title="Running"
          icon="repeat"
        />}
        <ButtonMenu
          route="/home/strategies"
          title="Strategies"
          icon="list"
        />
        <ButtonMenu
          route="/home/backtesting"
          title="Backtesting"
          icon="query_stats"
        />
        <ButtonMenu
          route="/home/exchanges"
          title="Exchanges"
          icon="currency_exchange"
        />
        <div className="logout" onClick={onLogout}>
          <i className="material-icons">power_settings_new</i>
        </div>
      </div>
    </TopbarStyle>
  )
}

export default Topbar
