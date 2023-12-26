import "../styles/registerView.css"

import React, { useState } from "react"

import ErrorModal from "../components/errorModal"
import { INVALID_EMAIL } from "../utils/interactiveMessages"
import SuccessModal from "../components/successModal"
import { createUser } from "../config/firebaseConfig"
import { useLocation } from "react-router-dom"
import { useRecoilState } from "recoil"
import { userState } from "../atoms/atoms"

const RegisterView = () => {
  const location = useLocation()
  const [user, setUser] = useRecoilState(userState)
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [investmentExperience, setInvestmentExperience] = useState("")
  const [dateOfBirth, setDateOfBirth] = useState("")
  const [address, setAddress] = useState("")
  const [occupation, setOccupation] = useState("")

  const [successModalOpen, setSuccessModalOpen] = useState(false)
  const [errorModalOpen, setErrorModalOpen] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")

  const handleCreateAccount = async () => {
    if (password.length < 6) {
      setErrorMessage("Password must be at least 6 characters long.")
      setErrorModalOpen(true)
      return
    }

    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match.")
      setErrorModalOpen(true)
      return
    }

    try {
      await createUser(email, password)
      setSuccessModalOpen(true)
    } catch (error) {
      if (error.message === INVALID_EMAIL) {
        setErrorMessage("The email you entered is not valid. Please try again.")
        setErrorModalOpen(true)
        return
      } else {
        setErrorMessage(
          "An error has occurred while registering. Please try again."
        )
        setErrorModalOpen(true)
        return
      }
    }
  }

  const handleCloseSuccessModal = () => {
    setSuccessModalOpen(false)
    setUser({
      user: {},
      isLoggedIn: true,
    })
    location.push("/home")
  }

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
            <span className="login-button" onClick={() => location.push("/")}>
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
      <ErrorModal
        isOpen={errorModalOpen}
        message={errorMessage}
        onClose={() => setErrorModalOpen(false)}
      />
    </div>
  )
}

export default RegisterView
