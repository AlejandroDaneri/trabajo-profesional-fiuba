/* Import Libs */
import { BrowserRouter, Route, Switch } from "react-router-dom"
import React from "react"
import { RecoilRoot } from "recoil"
import { Provider } from "react-redux"

/* Import Views */
import LoginView from "./views/loginView"
import RegisterView from "./views/registerView"

/* Import Styles */
import AppStyle from "./styles/app"
import HomeView from "./views/homeView"

import store from "./store"

/* Import Components */
import Popup from "./components/Popup"

const App = () => {
  return (
    <Provider store={store}>
      <RecoilRoot>
        <BrowserRouter>
          <AppStyle>
            <Popup />
            <Switch>
              <Route exact path="/" component={LoginView} />
              <Route path="/register" component={RegisterView} />
              <Route path="/home" component={HomeView} />
            </Switch>
          </AppStyle>
        </BrowserRouter>
      </RecoilRoot>
    </Provider>
  )
}

export default App
