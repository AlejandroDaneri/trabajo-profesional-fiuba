import styled from "styled-components"

export const TOPBAR_HEIGHT = "60px"

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
  height: ${TOPBAR_HEIGHT};

  & button {
    color: white;
  }

  & .logo {
    display: flex;
    align-items: center;
    justify-content: space-around;
    border: 1px solid white;
    border-radius: 10px;
    width: 160px;
    height: 40px;
    box-shadow: white 0px 2px 8px 0px;
    margin: 5px;
    margin-left: 20px;

    & img {
      width: 24px;
      height: 24px;
    }

    & p {
      font-size: 12px;
      font-weight: 600;
    }
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
