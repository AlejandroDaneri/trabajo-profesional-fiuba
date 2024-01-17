/* Import Libs */
import { useHistory } from "react-router-dom"
import {
  FaChartLine,
  FaExchangeAlt,
  FaSignOutAlt,
  FaUser,
} from "react-icons/fa"
import { useRecoilState } from "recoil"

/* Import Styles */
import TopbarStyle from "../styles/topbar"

/* Import Images */
import logo from "../images/bitcoin.png"

import { userState } from "../atoms/atoms"

const Topbar = () => {
  const history = useHistory()

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
        <button
          className="nav-button"
          onClick={() => history.push("/home/trades")}
        >
          <FaExchangeAlt className="nav-icon" />
          Trades
        </button>
        <button
          className="nav-button"
          onClick={() => history.push("/home/strategies")}
        >
          <FaExchangeAlt className="nav-icon" />
          Strategies
        </button>
        <button
          className="nav-button"
          onClick={() => history.push("/home/strategy")}
        >
          <FaExchangeAlt className="nav-icon" />
          Strategy
        </button>
        <button className="nav-button" onClick={onLogout}>
          <FaSignOutAlt className="nav-icon" /> Logout
        </button>
      </div>
    </TopbarStyle>
  )
}

export default Topbar
