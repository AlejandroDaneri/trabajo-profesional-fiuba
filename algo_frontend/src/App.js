import { BrowserRouter, Redirect, Route, Switch } from "react-router-dom";
import { RecoilRoot, useRecoilValue } from "recoil";

import AppStyle from "./styles/app";
import Home from "./components/home/Home";
import Login from "./components/Login";
import Popup from "./components/Popup";
import { Provider } from "react-redux";
import React from "react";
import store from "./store";
import { userState } from "./atoms/atoms";

const PrivateRoute = ({ component: Component, ...rest }) => {
  const user = useRecoilValue(userState);
  return (
    <Route
      {...rest}
      render={props =>
        user.isLoggedIn ? (
          <Component {...props} />
        ) : (
          <Redirect to="/" />
        )
      }
    />
  );
};

const App = () => {
  return (
    <Provider store={store}>
      <RecoilRoot>
        <BrowserRouter>
          <AppStyle>
            <Popup />
            <Switch>
              <Route exact path="/" component={Login} />
              <PrivateRoute path="/home" component={Home} />
            </Switch>
          </AppStyle>
        </BrowserRouter>
      </RecoilRoot>
    </Provider>
  );
};

export default App;
