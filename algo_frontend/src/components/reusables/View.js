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
    justify-content: space-between;
    padding: 0;
    margin: 0;
    width: 100%;
    height: 80px;
    border-top: 2px solid white;
    border-bottom: 2px solid white;
    background: #2d2d2d;

    & .header-button {
      display: flex;
      justify-content: center;
      align-items: center;
      border: 1px solid white;
      width: 100px;
      height: 30px;
      margin-right: 20px;

      &:hover {
        background: white;
        color: #282c34;
        cursor: pointer;
      }

      & i {
        font-size: 16px;
      }
    }

    & h1 {
      margin: 0;
      padding: 0;
      font-weight: 600;
      margin-left: 20px;
    }
  }
`

const View = ({ title, content, buttons }) => {
  return (
    <ViewStyle>
      <div className="header">
        <h1>{title}</h1>
        {buttons?.map((button) => (
          <div className="header-button" onClick={button.onClick}>
            {button.icon}
            {button.label}
          </div>
        ))}
      </div>
      <div className="content">{content}</div>
    </ViewStyle>
  )
}

export default View
