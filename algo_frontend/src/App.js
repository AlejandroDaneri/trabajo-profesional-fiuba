import "./styles/App.css";

import { BrowserRouter, Route, Routes } from "react-router-dom";

import LoginView from "./views/loginView";
import React from "react";
import { RecoilRoot } from "recoil";
import RegisterView from "./views/registerView";
import TopBar from "./components/topBar";
import TradesView from "./views/tradesView";
/* Import Libs */
import styled from "styled-components";

/* Import Components */

/* Import Images */

const AppStyle = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  background: #282c34;
  color: white;

  & .logo {
    display: flex;
    align-items: center;
    justify-content: space-around;
    border: 1px solid white;
    border-radius: 10px;
    width: 260px;
    height: 120px;
    margin: 20px;
    box-shadow: white 0px 2px 8px 0px;

    & img {
      height: 96px;
      height: 96px
      pointer-events: none;
    }

    & p {
      font-weight: 600;
    }
  }
`;

const App = () => {
  return (
    <div>
      <RecoilRoot>
        <BrowserRouter>
          <TopBar></TopBar>
          <Routes>
            <Route path="/" element={<LoginView />} />
            <Route path="/register" element={<RegisterView />} />
            <Route path="/trades" element={<TradesView />} />
          </Routes>
        </BrowserRouter>
      </RecoilRoot>
    </div>
  );
};

export default App;
