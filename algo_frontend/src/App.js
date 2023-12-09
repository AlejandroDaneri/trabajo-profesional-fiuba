import "./styles/App.css";

import { BrowserRouter, Route, Routes } from "react-router-dom";

import LoginView from "./views/loginView";
import React from "react";
import RegisterView from "./views/registerView";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginView />} />
          <Route path="/register" element={<RegisterView />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
