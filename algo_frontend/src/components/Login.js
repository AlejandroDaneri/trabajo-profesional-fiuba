/* Import Libs */
import React, { useEffect, useRef, useState } from "react"
import styled from "styled-components"
import { useHistory } from "react-router-dom"
import { useRecoilState } from "recoil"

/* Import Style */
import "../styles/loginView.css"

import { INVALID_EMAIL, WRONG_CREDENTIALS } from "../utils/interactiveMessages"
import { theme } from "../utils/theme"
import ErrorModal from "./errorModal"
import { login } from "../config/firebaseConfig"
import { userState } from "../atoms/atoms"

const images = require.context('../images/svg', true)
const imageList = images.keys().map(image => images(image))

const CryptoLogoStyle = styled.div`
  z-index: 0;
  position: absolute;
  left: ${({x}) => `${x}px`};
  top: ${({y}) => `${y}px`};
  right: 100px;

  @keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
  }

  & img {
    width: 50px;
    height: 50px;
    opacity: 0;
    animation: fadeIn 2s ease-in forwards;
    animation-delay: 1s;
  }
`

const CryptoLogo = ({ img }) => {
  const ref = useRef()

  const [state, stateFunc] = useState({
    x: 0,
    y: 0,
    show: true
  })

  useEffect(() => {
    const f = () => {
      const maxWidth = window.innerWidth - 60
      const maxHeight = window.innerHeight - 60

      const randomX = Math.floor(Math.random() * maxWidth)
      const randomY = Math.floor(Math.random() * maxHeight) 
      const show = (Math.floor(Math.random() * 5) + 1) === 1

      stateFunc({
        x: randomX,
        y: randomY,
        show: show
      })
    }
    const interval = setInterval(f, 5000)
    f()
    return () => {
      clearInterval(interval)
    }
  }, [])

  return state.show && <CryptoLogoStyle x={state.x} y={state.y}><img ref={ref} src={img} alt={'logo'} /></CryptoLogoStyle>
}

const LoginStyle = styled.div`
  display: flex;
  background: ${theme.dark};
  width: 100%;

  & .login-container {
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100vh;
    font-family: var(--primary-font);
    z-index: 1;
  }

  & .login-content {
    min-width: 35vw;
    padding: 40px;
    border-radius: 12px;
    background-color: ${theme.black};
    box-shadow: rgba(255, 255, 255, 0.35) 0px 0px 15px;

    & .login-additional-options {
      display: flex;
      justify-content: right;
    }
  }

  & .login-heading {
    text-align: center;
    color: ${theme.white};
    font-size: 36px;
    margin-bottom: 20px;
    animation: titleAnimation 0.8s ease;
  }
`

const LoginView = () => {
  const history = useHistory()

  const [user, setUser] = useRecoilState(userState)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [errorModal, setErrorModal] = useState({
    isOpen: false,
    message: "",
  })

  const handleCreateAccount = async () => {
    history.push("/register")
  }

  const handleLogin = async () => {
    try {
      await login(email, password)
      setUser({
        user: {},
        isLoggedIn: true,
      })
      history.push("/home/trades")
    } catch (error) {
      if (error.message === WRONG_CREDENTIALS) {
        setErrorModal({
          isOpen: true,
          message: "Invalid credentials. Please try again.",
        })
      } else if (error.message === INVALID_EMAIL) {
        setErrorModal({
          isOpen: true,
          message: "The email you entered is not valid. Please try again.",
        })
      } else {
        setErrorModal({
          isOpen: true,
          message: "An error has occurred while logging in. Please try again.",
        })
      }
    }
  }

  const closeErrorModal = () => {
    setErrorModal({
      isOpen: false,
      message: "",
    })
  }

  return (
    <LoginStyle>

      {imageList.map((image, index) => (
        <CryptoLogo key={index} img={image} alt={`image-${index}`} />
      ))}

      <div className="login-container">
        <div className="login-content">
          <h2 className="login-heading">¡Welcome to SatoshiBOT!</h2>
          <form className="login-form">
            <label className="login-label">Email</label>
            <input
              className="input-login-view"
              type="email"
              name="email"
              placeholder="Enter your email"
              onChange={(e) => setEmail(e.target.value)}
            />

            <label className="login-label">Password</label>
            <input
              className="input-login-view"
              type="password"
              name="password"
              placeholder="Enter your password"
              onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={handleLogin} type="button" className="login-btn">
              Log in
            </button>
          </form>

          <div className="login-additional-options">
            <button
              type="button"
              className="register-btn"
              onClick={handleCreateAccount}
            >
              Create your account
            </button>
          </div>
        </div>
        <ErrorModal
          isOpen={errorModal.isOpen}
          message={errorModal.message}
          onClose={closeErrorModal}
        />
      </div>
    </LoginStyle>
  )
}

export default LoginView
