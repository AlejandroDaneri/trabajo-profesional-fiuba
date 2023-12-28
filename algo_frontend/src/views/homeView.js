import { Route } from "react-router-dom"
import Topbar from "../components/topbar"
import TradesView from "./tradesView"
import StrategyView from "./strategyView"

const HomeView = () => {
  return (
    <>
      <Topbar />
      <div className="content">
        <Route exact path="/home/trades" component={TradesView} />
        <Route exact path="/home/strategy" component={StrategyView} />
      </div>
    </>
  )
}

export default HomeView
