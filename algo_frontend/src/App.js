import "./styles/App.css";

import { BrowserRouter, Route, Routes } from "react-router-dom";

import LoginView from "./views/loginView";
import React from "react";
import { RecoilRoot } from "recoil";
import RegisterView from "./views/registerView";
import TopBar from "./components/topBar";
import TradesView from "./views/tradesView";

function App() {
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
}

export default App;
