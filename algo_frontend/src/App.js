import "./styles/App.css";

import React, { useState } from "react";
import { createUser, login } from "./config/firebaseConfig";

import logo from "./assets/bitcoin.png";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    await createUser(email, password);
  };

  const handleLogin = async () => {
    await login(email, password);
  };

  return (
    <div className="App">
      <div className="Login-area">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
        <button onClick={handleLogin}>Login</button>
      </div>
      <img src={logo} className="App-logo" alt="logo" />
      <p>SatoshiBOT.tech </p>
    </div>
  );
}

export default App;
