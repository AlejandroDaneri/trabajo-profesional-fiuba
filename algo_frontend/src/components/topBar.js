import "../styles/topBar.css";

import { FaExchangeAlt, FaUser } from "react-icons/fa";

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
      </div>
    </div>
  );
};

export default TopBar;
