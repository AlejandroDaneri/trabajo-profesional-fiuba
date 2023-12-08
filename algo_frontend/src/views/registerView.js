import "../styles/registerView.css";

import React, { useState } from "react";

const RegisterView = () => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [investmentExperience, setInvestmentExperience] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [address, setAddress] = useState("");
  const [occupation, setOccupation] = useState("");

  const handleCreateAccount = async () => {
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    //CreateUser
  };

  return (
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
          <span className="login-button">Log In</span>
        </p>
      </form>
    </div>
  );
};

export default RegisterView;
