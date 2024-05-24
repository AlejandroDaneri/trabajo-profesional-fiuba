/* Import Libs */
import { Route } from "react-router-dom"

/* Import Components */
import Topbar from "./Topbar"
import CurrentStrategy from "../CurrentStrategy"
import Strategies from "./strategies/Strategies"
import Backtesting from "./backtesting/Backtesting"
import Exchanges from "./exchanges/Exchanges"

const Home = () => {
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

export default Home
