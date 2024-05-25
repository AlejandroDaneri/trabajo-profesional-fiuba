/* Import Libs */
import { BrowserRouter, Route, Switch } from "react-router-dom"
import React from "react"
import { RecoilRoot } from "recoil"
import { Provider } from "react-redux"

/* Import Components */
import Login from "./components/Login"
import Home from "./components/home/Home"
import Popup from "./components/Popup"

/* Import Styles */
import AppStyle from "./styles/app"

import store from "./store"

const App = () => {
  return (
    <Provider store={store}>
      <RecoilRoot>
        <BrowserRouter>
          <AppStyle>
            <Popup />
            <Switch>
              <Route exact path="/" component={Login} />
              <Route path="/home" component={Home} />
            </Switch>
          </AppStyle>
        </BrowserRouter>
      </RecoilRoot>
    </Provider>
  )
}

export default App
