/* Import Libs */
import { useHistory } from "react-router-dom"
import { useRecoilState } from "recoil"
import styled from "styled-components"
import { useLocation } from "react-router-dom"

/* Import Styles */
import TopbarStyle from "../styles/topbar"

/* Import Images */
import logo from "../images/bitcoin.png"

import { userState } from "../atoms/atoms"
import { theme } from "../utils/theme"

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

  // eslint-disable-next-line
  const [user, setUser] = useRecoilState(userState)

  const onLogout = () => {
    setUser({
      user: {},
      isLoggedIn: false,
    })
    history.push("/")
  }

  return (
    <TopbarStyle>
      <div className="logo">
        <img src={logo} className="App-logo" alt="logo" />
        <p>SatoshiBOT.tech</p>
      </div>
      <div className="nav-links">
        <ButtonMenu route="/home/trades" title="Running" icon="repeat" />
        <ButtonMenu route="/home/strategies" title="Strategies" icon="list" />
        <ButtonMenu route="/home/exchanges" title="Exchanges" icon="currency_exchange" />
        <div className="logout" onClick={onLogout}>
          <i className="material-icons">power_settings_new</i>
        </div>
      </div>
    </TopbarStyle>
  )
}

export default Topbar
