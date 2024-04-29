import styled from "styled-components"
import { theme } from "../utils/theme"

export const TOPBAR_HEIGHT = "40px"

const TopbarStyle = styled.div`
  display: flex;
  align-self: start;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s;
  background: ${theme.dark};
  color: ${theme.white};
  text-color: ${theme.white};
  width: 100%;
  height: ${TOPBAR_HEIGHT};

  & .logout {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 80px;
    cursor: pointer;

    &:hover {
      background: ${theme.red};
    }
  }

  & button {
    color: ${theme.white};
  }

  & .logo {
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid ${theme.white};
    border-radius: 10px;
    width: 160px;
    height: 25px;
    box-shadow: ${theme.white} 0px 0px 2px 1px;
    margin: 5px;
    margin-left: 20px;

    & img {
      width: 18px;
      height: 18px;
      margin-right: 10px;
    }

    & p {
      font-size: 12px;
      font-weight: 600;
    }
  }

  & .nav-links {
    display: flex;
    height: 100%;
  }
`

export default TopbarStyle
