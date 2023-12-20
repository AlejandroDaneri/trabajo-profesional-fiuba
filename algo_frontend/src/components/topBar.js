import "../styles/topBar.css";

import {
  FaChartLine,
  FaExchangeAlt,
  FaSignOutAlt,
  FaUser,
} from "react-icons/fa";

import React from "react";
import { useNavigate } from "react-router-dom";
import { useRecoilState } from "recoil";
import { userState } from "../atoms/atoms";

const TopBar = () => {
  let navigate = useNavigate();
  const [user, setUser] = useRecoilState(userState);

  if (!user.isLoggedIn) {
    return null;
  }

  const handleLogOut = () => {
    setUser({
      user: {},
      isLoggedIn: false,
    });
    navigate("/");
  };

  return (
    <div className="top-bar">
      <div className="logo">SatoshiBot</div>
      <div className="nav-links">
        <button className="nav-button" onClick={() => navigate("/trades")}>
          <FaExchangeAlt className="nav-icon" /> Trades
        </button>
        <button className="nav-button" onClick={() => navigate("/graphs")}>
          <FaChartLine className="nav-icon" /> Graphs
        </button>
        <button
          className="nav-button"
          onClick={() => console.log("Profile clicked")}
        >
          <FaUser className="nav-icon" /> Profile
        </button>
        <button className="nav-button" onClick={() => handleLogOut()}>
          <FaSignOutAlt className="nav-icon" /> Logout
        </button>
      </div>
    </div>
  );
};

export default TopBar;
