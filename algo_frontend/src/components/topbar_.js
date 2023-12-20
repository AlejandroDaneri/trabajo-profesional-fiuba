/* Import Libs */
import { useNavigate } from "react-router-dom"
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
  const navigate = useNavigate()
  const [user, setUser] = useRecoilState(userState)

  const onLogout = () => {
    setUser({
      user: {},
      isLoggedIn: false,
    })
    navigate("/")
  }

  return (
    <TopbarStyle>
      <div className="logo">
        <img src={logo} className="App-logo" alt="logo" />
        <p>SatoshiBOT.tech</p>
      </div>
      <div className="nav-links">
        <button className="nav-button" onClick={() => navigate("/home")}>
          <FaExchangeAlt className="nav-icon" />
          Trades
        </button>
        <button className="nav-button" onClick={() => navigate("/graphs")}>
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
