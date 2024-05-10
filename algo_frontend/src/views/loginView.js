import "../styles/loginView.css";

import { INVALID_EMAIL, WRONG_CREDENTIALS } from "../utils/interactiveMessages";
import React, { useState } from "react";

import ErrorModal from "../components/errorModal";
import { login } from "../config/firebaseConfig";
import { useHistory } from "react-router-dom";
import { useRecoilState } from "recoil";
import { userState } from "../atoms/atoms";

const LoginView = () => {
  const history = useHistory();

  const [user, setUser] = useRecoilState(userState);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorModal, setErrorModal] = useState({
    isOpen: false,
    message: "",
  });

  const handleCreateAccount = async () => {
    history.push("/register");
  };

  const handleLogin = async () => {
    try {
      await login(email, password);
      setUser({
        user: {},
        isLoggedIn: true,
      });
      history.push("/home/trades");
    } catch (error) {
      if (error.message === WRONG_CREDENTIALS) {
        setErrorModal({
          isOpen: true,
          message: "Invalid credentials. Please try again.",
        });
      } else if (error.message === INVALID_EMAIL) {
        setErrorModal({
          isOpen: true,
          message: "The email you entered is not valid. Please try again.",
        });
      } else {
        setErrorModal({
          isOpen: true,
          message: "An error has occurred while logging in. Please try again.",
        });
      }
    }
  };

  const closeErrorModal = () => {
    setErrorModal({
      isOpen: false,
      message: "",
    });
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <h2 className="login-heading">¡Welcome to SatoshiBot!</h2>
        <form className="login-form">
          <label className="login-label">Email</label>
          <input
            className="input-login-view"
            type="email"
            name="email"
            placeholder="Enter your email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <label className="login-label">Password</label>
          <input
            className="input-login-view"
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
      <ErrorModal
        isOpen={errorModal.isOpen}
        message={errorModal.message}
        onClose={closeErrorModal}
      />
    </div>
  );
};

export default LoginView;
