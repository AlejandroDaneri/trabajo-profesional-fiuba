import styled from "styled-components"

const StrategiesStyle = styled.div`
  display: flex;
  align-items: center;
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

    & .currency {
      margin-right: 5px;
    }
  }

  & .actions {
    display: flex;
    justify-content: center;
  }
`

export default StrategiesStyle
