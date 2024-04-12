import styled from "styled-components"

const StrategiesStyle = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 100%;
  height: 90%;
  padding: 20px;

  & .state {
    display: flex;
    justify-content: center;
    align-items: center;
    max-height: 35px;

    & .loader {
      margin-left: 5px;
      max-height: 35px;
    }
  }

  & .indicator-content {
    width: 200px;
    background: #282c34;

    & .parameter {
      display: flex;
      border-bottom: 1px solid white;
    }
  }

  & .indicators {
    display: flex;
    flex-direction: row;
    justify-content: center;

    & .indicator-button {
      background: white;
      color: #282c34;
      padding: 3px;
      cursor: pointer;
      font-size: 12px;
      margin-right: 10px;
    }
  }

  & .currencies {
    display: flex;
    flex-direction: row;
    justify-content: center;

    & .currency {
      margin-right: 5px;
    }
  }

  & .actions {
    display: flex;
    justify-content: center;

    & .button-container {
      cursor: pointer;
      margin-right: 10px;
    }
  }
`

export default StrategiesStyle
