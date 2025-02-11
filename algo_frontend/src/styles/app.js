import styled from "styled-components"
import { theme } from "../utils/theme"

const AppStyle = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  background: ${theme.grayDark};
  color: white;

  & .content {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }
`

export default AppStyle
