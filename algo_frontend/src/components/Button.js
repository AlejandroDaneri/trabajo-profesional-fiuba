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

const Button = ({ text, onClick, loading }) => {
  return (
    <ButtonStyle onClick={onClick}>{loading ? "loading" : text}</ButtonStyle>
  )
}

export default Button
