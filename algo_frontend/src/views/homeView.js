/* Import Libs */
import { Route } from "react-router-dom"

/* Import Components */
import Topbar from "../components/topbar"

/* Import Views */
import CurrentStrategy from "./CurrentStrategy"
import Strategies from "./Strategies"

const HomeView = () => {
  return (
    <>
      <Topbar />
      <div className="content">
        <Route exact path="/home/trades" component={CurrentStrategy} />
        <Route exact path="/home/strategies" component={Strategies} />
      </div>
    </>
  )
}

export default HomeView
