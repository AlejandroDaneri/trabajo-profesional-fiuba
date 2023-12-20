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
`

export default AppStyle
