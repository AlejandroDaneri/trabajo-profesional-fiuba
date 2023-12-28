/* Import Libs */
import styled from "styled-components"

const StrategyStyle = styled.div`
  display: flex;

  & .currencies {
    display: flex;
    flex-direction: column;
    border: 1px solid white;
    border-radius: 10px;
    padding: 10px;
    margin-right: 10px;

    & .coin {
      display: flex;
      align-items: center;
      justify-content: space-around;
      width: 100px;

      & img {
        width: 24px;
        height: 24px;
        margin-right: 5px;
        border-radius: 30px;
      }
    }
  }

  & .indicators {
    display: flex;
    flex-direction: column;
    border: 1px solid white;
    border-radius: 10px;
    padding: 10px;

    & .indicator {
      border: 1px solid white;
      border-radius: 10px;
      padding: 10px;
      margin: 10px;

      & .name {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 5px;
      }

      & .parameters {
        display: flex;
        flex-direction: column;
      }
    }
  }
`

export default StrategyStyle
