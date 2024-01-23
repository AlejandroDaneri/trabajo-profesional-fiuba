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

const ButtonMenuStyle = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${({ selected }) => (selected ? "#F7931A" : "black")};
  cursor: pointer;
  transition: color 0.3s;
  height: 100%;
  width: 200px;
  border: none;

  & p {
    font-size: 16px;
    font-weight: 600;
    color: ${({ selected }) => (selected ? "#000000" : "#ffffff")};
  }
`

const ButtonMenu = ({ route, title }) => {
  const history = useHistory()
  const location = useLocation()
  return (
    <ButtonMenuStyle
      onClick={() => history.push(route)}
      selected={location.pathname === route}
    >
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
        <ButtonMenu route="/home/trades" title="Current Strategy" />
        <ButtonMenu route="/home/strategies" title="Strategies" />
        <ButtonMenu route="/home/strategy" title="Strategy" />
      </div>
    </TopbarStyle>
  )
}

export default Topbar
