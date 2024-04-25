/* Import Libs */
import { Route } from "react-router-dom"

/* Import Components */
import Topbar from "../components/topbar"

/* Import Views */
import CurrentStrategy from "./CurrentStrategy"
import Strategies from "./Strategies"
import Backtesting from "./Backtesting"
import Exchanges from "./Exchanges"

const HomeView = () => {
  return (
    <>
      <Topbar />
      <div className="content">
        <Route exact path="/home/trades" component={CurrentStrategy} />
        <Route exact path="/home/strategies" component={Strategies} />
        <Route exact path="/home/backtesting" component={Backtesting} />
        <Route exact path="/home/exchanges" component={Exchanges} />
      </div>
    </>
  )
}

export default HomeView
