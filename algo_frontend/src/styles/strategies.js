import styled from "styled-components"

const StrategiesStyle = styled.div`
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

    & h1 {
      margin: 0;
      padding: 0;
      font-weight: 600;
      margin-left: 20px;
    }
  }

  & .strategies {
    display: flex;
    flex-direction: column;
    width: 80%;

    & .indicators {
      display: flex;
      flex-direction: row;
      justify-content: center;

      & .indicator {
        background: white;
        color: black;
        padding: 3px;
      }
    }

    & .currencies {
      display: flex;
      flex-direction: row;
      justify-content: center;
    }

    & .actions {
      display: flex;
      justify-content: center;
    }
  }
`

export default StrategiesStyle
