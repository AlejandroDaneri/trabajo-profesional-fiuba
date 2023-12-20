import "../styles/successModal.css";

import { FaCheckCircle, FaTimes } from "react-icons/fa";

import React from "react";

const SuccessModal = ({ isOpen, message, onClose }) => {
  return (
    <div className={`success-modal ${isOpen ? "open" : ""}`}>
      <div className="modal-content">
        <span className="close-btn" onClick={onClose}>
          <FaTimes />
        </span>
        <FaCheckCircle className="success-icon" />
        <p className="success-message">{message}</p>
      </div>
    </div>
  );
};

export default SuccessModal;
