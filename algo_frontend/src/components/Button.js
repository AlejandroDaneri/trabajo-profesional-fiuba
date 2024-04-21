import styled from "styled-components"
import { theme } from "../utils/theme"

const ButtonStyle = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid white;
  width: ${({ width }) => width || 100}px;
  height: ${({ height }) => height || 26}px;
  cursor: pointer;
  border-radius: ${({ circle }) => circle && "30px"};

  & i {
    color: white;
    font-size: 16px;
  }

  &:hover {
    background: white;
    color: ${theme.grayDark};

    & i {
      color: ${theme.grayDark};
    }
  }
`

const Button = ({ text, onClick, loading, width, height, circle, tooltip }) => {
  return (
    <ButtonStyle
      onClick={onClick}
      width={width}
      height={height}
      circle={circle}
      title={tooltip}
    >
      {loading ? "loading" : text}
    </ButtonStyle>
  )
}

export default Button
