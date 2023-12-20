import Topbar from "../components/topbar_"
import TradesView from "./tradesView"

const HomeView = () => {
  return (
    <>
      <Topbar />
      <div className="content">
        <TradesView />
      </div>
    </>
  )
}

export default HomeView
