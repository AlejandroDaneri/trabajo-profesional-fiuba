import styled from "styled-components"
import { TOPBAR_HEIGHT } from "./topbar"

const AppStyle = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  background: #282c34;
  color: white;

  & .content {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: calc(100vh - ${TOPBAR_HEIGHT});
  }

  & .logo {
    display: flex;
    align-items: center;
    justify-content: space-around;
    border: 1px solid white;
    border-radius: 10px;
    width: 260px;
    height: 120px;
    margin: 20px;
    box-shadow: white 0px 2px 8px 0px;

    & img {
      height: 96px;
      height: 96px
      pointer-events: none;
    }

    & p {
      font-weight: 600;
    }
  }
`

export default AppStyle
