/* Import Style */
import "../styles/registerView.css"
import styled from "styled-components"

/* Import Libs */
import React, { useState } from "react"

/* Import Components */
import ErrorModal from "../components/errorModal"
/* Import Utils */
import { INVALID_EMAIL } from "../utils/interactiveMessages"
import SuccessModal from "../components/successModal"
import { createUser } from "../config/firebaseConfig"
import { useHistory } from "react-router-dom"
import { theme } from "../utils/theme"

const RegisterViewStyle = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 100vh;
  font-family: var(--primary-font);
  margin: 0;
  background: ${theme.dark};

  & .register-container {
    min-height: 50vh;
    min-width: 35vw;
    padding: 20px 40px 20px 40px;
    margin-top: 5vh;
    margin-bottom: 5vh;
    border-radius: 12px;
    background-color: var(--background-light);
    text-align: center;
    background-color: ${theme.black};
    box-shadow: rgba(255, 255, 255, 0.35) 0px 0px 15px;

    & .already-have-account-text {
      color: ${theme.white};
      font-size: 14px;
    }

    & .register-labels {
      margin-bottom: 8px;
      font-weight: bold;
      color: ${theme.white};
    }
  }
`

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
    <RegisterViewStyle>
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
    </RegisterViewStyle>
  )
}

export default RegisterView
