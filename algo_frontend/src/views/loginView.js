import "../styles/loginView.css";

import React, { useState } from "react";
import { createUser, login } from "../config/firebaseConfig";

const LoginView = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleCreateAccount = async () => {
    await createUser(email, password);
  };

  const handleLogin = async () => {
    await login(email, password);
  };
  return (
    <div className="login-container">
      <h2>¡Welcome to SatoshiBot!</h2>
      <form>
        <label>Email</label>
        <input
          type="email"
          name="email"
          placeholder="Enter your email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <label>Password</label>
        <input
          type="password"
          name="password"
          placeholder="Enter your password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleLogin} type="button" className="login-button">
          Log in
        </button>
      </form>

      <div className="login-options">
        <button type="button" className="forgot-password-button">
          Forgot your password?
        </button>
        <button
          type="button"
          className="register-button"
          onClick={handleCreateAccount}
        >
          Create your account
        </button>
      </div>
    </div>
  );
};

export default LoginView;
