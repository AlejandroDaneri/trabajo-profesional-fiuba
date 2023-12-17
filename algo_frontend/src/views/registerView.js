import "../styles/registerView.css";

import React, { useState } from "react";

import SuccessModal from "../components/successModal";
import { createUser } from "../config/firebaseConfig";
import { useNavigate } from "react-router-dom";
import { useRecoilState } from "recoil";
import { userState } from "../atoms/atoms";

const RegisterView = () => {
  const navigate = useNavigate();
  const [user, setUser] = useRecoilState(userState);
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [investmentExperience, setInvestmentExperience] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [address, setAddress] = useState("");
  const [occupation, setOccupation] = useState("");

  const [successModalOpen, setSuccessModalOpen] = useState(false);

  const handleCreateAccount = async () => {
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    try {
      await createUser(email, password);
      setSuccessModalOpen(true);
    } catch (error) {
      console.error("Error creating user:", error);
    }
  };

  const handleCloseSuccessModal = () => {
    setSuccessModalOpen(false);
    setUser({
      user: {},
      isLoggedIn: true,
    });
    navigate("/trades");
  };

  return (
    <div className="register-page-container">
      <div className="register-container">
        <h2>Create Your Account</h2>
        <form>
          <label>Full Name</label>
          <input
            type="text"
            name="fullName"
            placeholder="Enter your full name"
            onChange={(e) => setFullName(e.target.value)}
          />

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

          <label>Confirm Password</label>
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm your password"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />

          <label>Investment Experience</label>
          <select
            name="investmentExperience"
            onChange={(e) => setInvestmentExperience(e.target.value)}
          >
            <option value="">Select your experience level</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>

          <label>Date of Birth</label>
          <input
            type="date"
            name="dateOfBirth"
            onChange={(e) => setDateOfBirth(e.target.value)}
          />

          <label>Address</label>
          <input
            type="text"
            name="address"
            placeholder="Enter your address"
            onChange={(e) => setAddress(e.target.value)}
          />

          <label>Occupation</label>
          <input
            type="text"
            name="occupation"
            placeholder="Enter your occupation"
            onChange={(e) => setOccupation(e.target.value)}
          />

          <button
            onClick={handleCreateAccount}
            type="button"
            className="register-button"
          >
            Create Account
          </button>
          <p className="login-options">
            <span>Already have an account?</span>
            <span className="login-button" onClick={() => navigate("/")}>
              Log In
            </span>
          </p>
        </form>
      </div>
      <SuccessModal
        isOpen={successModalOpen}
        message="User created successfully!"
        onClose={handleCloseSuccessModal}
      />
    </div>
  );
};

export default RegisterView;
