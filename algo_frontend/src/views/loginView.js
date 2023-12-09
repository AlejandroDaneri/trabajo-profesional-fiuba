import "../styles/loginView.css";

import React, { useState } from "react";

import { login } from "../config/firebaseConfig";
import { useNavigate } from "react-router-dom";

const LoginView = () => {
  let navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleCreateAccount = async () => {
    navigate("/register");
  };

  const handleLogin = async () => {
    await login(email, password);
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <h2 className="login-heading">¡Welcome to SatoshiBot!</h2>
        <form className="login-form">
          <label className="login-label">Email</label>
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <label className="login-label">Password</label>
          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button onClick={handleLogin} type="button" className="login-btn">
            Log in
          </button>
        </form>

        <div className="login-additional-options">
          <button type="button" className="forgot-password-btn">
            Forgot your password?
          </button>
          <button
            type="button"
            className="register-btn"
            onClick={handleCreateAccount}
          >
            Create your account
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginView;
