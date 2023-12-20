/* Import Libs */
import { BrowserRouter, Route, Routes } from "react-router-dom"
import React from "react"
import { RecoilRoot } from "recoil"

//import GraphsView from "./views/graphsView";
//<Route path="/graphs" element={<GraphsView />} />

/* Import Views */
import LoginView from "./views/loginView"
import RegisterView from "./views/registerView"

/* Import Styles */
import AppStyle from "./styles/app"
import HomeView from "./views/homeView"

const App = () => {
  return (
    <RecoilRoot>
      <BrowserRouter>
        <AppStyle>
          <Routes>
            <Route exact path="/" element={<LoginView />} />
            <Route exact path="/register" element={<RegisterView />} />
            <Route path="/home" element={<HomeView />} />
          </Routes>
        </AppStyle>
      </BrowserRouter>
    </RecoilRoot>
  )
}

export default App
