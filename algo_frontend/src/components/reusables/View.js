import styled from "styled-components"
import BounceLoader from "react-spinners/BounceLoader"
import { theme } from "../../utils/theme"

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
    border-top: 2px solid ${theme.white};
    border-bottom: 2px solid ${theme.white};
    background: ${theme.black};
    color: ${theme.white};

    & h1 {
      display: flex;
      align-items: center;

      & .loader {
        margin-left: 10px;
      }
    }

    & .header-button {
      display: flex;
      justify-content: center;
      align-items: center;
      border: 1px solid ${theme.white};
      width: 100px;
      height: 30px;
      margin-right: 20px;

      & p {
        margin-left: 5px;
      }

      &:hover {
        background: ${theme.white};
        color: ${theme.grayDark};
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

const View = ({ title, content, buttons, loading }) => {
  return (
    <ViewStyle>
      <div className="header">
        <h1>{title} {loading && <div className="loader"><BounceLoader color="white" size={32} /></div>}</h1>
        {buttons?.map((button) => (
          <div className="header-button" onClick={button.onClick}>
            {button.icon}
            <p>{button.label}</p>
          </div>
        ))}
      </div>
      <div className="content">{content}</div>
    </ViewStyle>
  )
}

export default View
