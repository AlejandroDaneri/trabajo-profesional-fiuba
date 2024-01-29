import styled from "styled-components"

const ButtonStyle = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid white;
  width: 100px;
  cursor: pointer;

  &:hover {
    background: white;
    color: #282c34;
  }
`

const Button = ({ text, onClick }) => {
  return <ButtonStyle onClick={onClick}>{text}</ButtonStyle>
}

export default Button
