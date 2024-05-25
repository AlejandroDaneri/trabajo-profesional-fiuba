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
  border: none;
  border-top: ${({ selected }) => (selected ? `5px solid ${theme.btc}` : `0px solid ${theme.dark}`)};
  background: ${theme.dark};
  cursor: pointer;
  transition: color 0.3s;
  height: 100%;
  width: 200px;
  transition: border-top 0.5s ease;

  & i {
    margin-right: 10px;
    font-size: 22px;
    padding: 0;
    color: ${theme.white};
  }

  & p {
    font-size: 14px;
    font-weight: 600;
    color: ${theme.white};
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
