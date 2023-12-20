import styled from "styled-components"

export const TOPBAR_HEIGHT = "40px"

const TopbarStyle = styled.div`
  display: flex;
  align-self: start;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s;
  background: black;
  color: white;
  text-color: white;
  width: 100%;
  height: 40px;

  & button {
    color: white;
  }

  & .logo_ {
    font-size: 1.7rem;
    font-weight: bold;
    transition: color 0.3s;
  }

  & .nav-links {
    display: flex;
  }

  & .nav-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    margin-right: 20px;
    transition: color 0.3s;
    font-size: 1rem;
  }

  & .nav-button:hover {
  }

  & .nav-button svg {
    margin-right: 8px;
  }

  & .nav-button svg:hover {
  }
`

export default TopbarStyle
