/* Import Style */
import "../styles/registerView.css"

/* Import Libs */
import React, { useState } from "react"

/* Import Components */
import ErrorModal from "../components/errorModal"
/* Import Utils */
import { INVALID_EMAIL } from "../utils/interactiveMessages"
import SuccessModal from "../components/successModal"
import { createUser } from "../config/firebaseConfig"
import { useHistory } from "react-router-dom"

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
        <h2 className="create-account-heading">Create Your Account</h2>
        <form>
          <label className="register-labels">Email</label>
          <input
            className="input-register-view"
            type="email"
            name="email"
            placeholder="Enter your email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <label className="register-labels">Password</label>
          <input
            className="input-register-view"
            type="password"
            name="password"
            placeholder="Enter your password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <label className="register-labels">Confirm Password</label>
          <input
            className="input-register-view"
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
            <span className="already-have-account-text">
              Already have an account?
            </span>
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
