import styled from "styled-components"

const ViewStyle = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;

  & .header {
    display: flex;
    align-items: center;
    padding: 0;
    margin: 0;
    width: 100%;
    height: 80px;
    border-top: 2px solid white;
    border-bottom: 2px solid white;
    background: #2d2d2d;

    & h1 {
      margin: 0;
      padding: 0;
      font-weight: 600;
      margin-left: 20px;
    }
  }
`

const View = ({ title, content }) => {
  return (
    <ViewStyle>
      <div className="header">
        <h1>{title}</h1>
      </div>
      <div className="content">{content}</div>
    </ViewStyle>
  )
}

export default View
