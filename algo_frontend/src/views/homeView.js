/* Import Libs */
import { Route } from "react-router-dom"

/* Import Components */
import Topbar from "../components/topbar"

/* Import Views */
import TradesView from "./tradesView"
import StrategiesView from "./strategiesView"
import StrategyView from "./strategyView"

const HomeView = () => {
  return (
    <>
      <Topbar />
      <div className="content">
        <Route exact path="/home/trades" component={TradesView} />
        <Route exact path="/home/strategies" component={StrategiesView} />
        <Route exact path="/home/strategy" component={StrategyView} />
      </div>
    </>
  )
}

export default HomeView
