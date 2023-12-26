/* Import Libs */
import React, { useState } from "react"
import { useHistory } from "react-router-dom"

/* Import Components */
import ErrorModal from "../components/errorModal"
import SuccessModal from "../components/successModal"

/* Import Utils */
import { INVALID_EMAIL } from "../utils/interactiveMessages"

/* Import Style */
import "../styles/registerView.css"

import { createUser } from "../config/firebaseConfig"

const RegisterView = () => {
  const history = useHistory()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

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
    history.push("/home/trades")
  }

  return (
    <div className="register-page-container">
      <div className="register-container">
        <h2>Create Your Account</h2>
        <form>
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

          <button
            onClick={handleCreateAccount}
            type="button"
            className="register-button"
          >
            Create Account
          </button>
          <p className="login-options">
            <span>Already have an account?</span>
            <span className="login-button" onClick={() => history.push("/")}>
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
