import "../styles/topBar.css";

import { FaExchangeAlt, FaSignOutAlt, FaUser } from "react-icons/fa";

import React from "react";

const TopBar = () => {
  return (
    <div className="top-bar">
      <div className="logo">SatoshiBot</div>
      <div className="nav-links">
        <button
          className="nav-button"
          onClick={() => console.log("Trades clicked")}
        >
          <FaExchangeAlt className="nav-icon" /> Trades
        </button>
        <button
          className="nav-button"
          onClick={() => console.log("Profile clicked")}
        >
          <FaUser className="nav-icon" /> Profile
        </button>
        <button
          className="nav-button"
          onClick={() => console.log("Logout clicked")}
        >
          <FaSignOutAlt className="nav-icon" /> Logout
        </button>
      </div>
    </div>
  );
};

export default TopBar;
