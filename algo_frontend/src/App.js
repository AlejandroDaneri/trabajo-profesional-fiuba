import "./styles/App.css";

import { BrowserRouter, Route, Routes } from "react-router-dom";

import GraphsView from "./views/graphsView";
import LoginView from "./views/loginView";
import React from "react";
import { RecoilRoot } from "recoil";
import RegisterView from "./views/registerView";
import TopBar from "./components/topBar";
import TradesView from "./views/tradesView";

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
            <Route path="/graphs" element={<GraphsView />} />
          </Routes>
        </BrowserRouter>
      </RecoilRoot>
    </div>
  );
};

export default App;
