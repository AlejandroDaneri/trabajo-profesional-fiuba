import "../styles/errorModal.css";

import { FaExclamationCircle, FaTimes } from "react-icons/fa";

import React from "react";

const ErrorModal = ({ isOpen, message, onClose }) => {
  return (
    <div className={`error-modal ${isOpen ? "open" : ""}`}>
      <div className="modal-content">
        <span className="close-btn" onClick={onClose}>
          <FaTimes />
        </span>
        <FaExclamationCircle className="error-icon" />
        <p className="error-message">{message}</p>
      </div>
    </div>
  );
};

export default ErrorModal;
