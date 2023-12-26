/* Import Libs */
import { useHistory } from "react-router-dom"
import {
  FaChartLine,
  FaExchangeAlt,
  FaSignOutAlt,
  FaUser,
} from "react-icons/fa"
import TopbarStyle from "../styles/topbar"
import { useRecoilState } from "recoil"
import { userState } from "../atoms/atoms"
import logo from "../images/bitcoin.png"

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
          onClick={() => history.push("/home/strategy")}
        >
          <FaExchangeAlt className="nav-icon" />
          Strategy
        </button>
        <button className="nav-button" onClick={() => history.push("/graphs")}>
          <FaChartLine className="nav-icon" />
          Graphs
        </button>
        <button
          className="nav-button"
          onClick={() => console.log("Profile clicked")}
        >
          <FaUser className="nav-icon" /> Profile
        </button>
        <button className="nav-button" onClick={onLogout}>
          <FaSignOutAlt className="nav-icon" /> Logout
        </button>
      </div>
    </TopbarStyle>
  )
}

export default Topbar
