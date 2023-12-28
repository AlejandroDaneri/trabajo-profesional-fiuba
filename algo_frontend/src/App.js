/* Import Libs */
import { BrowserRouter, Route, Switch } from "react-router-dom"
import React from "react"
import { RecoilRoot } from "recoil"

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
          <Switch>
            <Route exact path="/" component={LoginView} />
            <Route path="/register" component={RegisterView} />
            <Route path="/home" component={HomeView} />
          </Switch>
        </AppStyle>
      </BrowserRouter>
    </RecoilRoot>
  )
}

export default App
