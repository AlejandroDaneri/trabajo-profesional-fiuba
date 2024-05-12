import styled from "styled-components"
import { theme } from "../utils/theme"

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
    background: ${theme.grayDark};

    & .parameter {
      display: flex;
      border-bottom: 1px solid white;
    }
  }

  & .exchange-info {
    display: flex;
    justify-content: center;

    p {
      margin: 0;
    }

    & img {
      margin: 0;
      margin-left: 5px;
      padding: 0;
    }
  }

  & .indicators {
    display: flex;
    flex-direction: row;
    justify-content: center;

    & .indicator-button {
      background: ${theme.white};
      color: ${theme.grayDark};
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
