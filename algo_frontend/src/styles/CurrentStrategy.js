import styled from "styled-components"

export const ResultStyle = styled.div`
  color: ${({ win }) => (win ? "green" : "red")};
  font-weight: 600;
`

export const CurrentStrategyStyle = styled.div`
  height: 100%;
  width: 90%;

  & .summary {
    height: 120px;
    width: 100%;

    & .summary-content {
      display: flex;
      flex-direction: row;
      width: 50%;
      justify-content: space-around;
  
      & .box {
        display: flex;
        flex-direction: column;
        border: 1px solid white;
        padding: 10px;
  
        & .label {
          color: #a5a8b6;
        }
  
        & .value {
          font-weight: 800;
        }
      }
    }
  }

  & .trades {
    height: calc(100% - 120px - 80px);
    width: 100%;
  }
`
