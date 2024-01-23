import styled from "styled-components"

export const ResultStyle = styled.div`
  color: ${({ win }) => (win ? "green" : "red")};
  font-weight: 600;
`

export const CurrentStrategyStyle = styled.div`
  & .summary {
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

  & .trades {
    overflow-y: scroll;
    width: 80%;

    &::-webkit-scrollbar {
      width: 5px;
    }

    &::-webkit-scrollbar-track {
      box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    }

    &::-webkit-scrollbar-thumb {
      background-color: darkgrey;
      outline: 1px solid slategrey;
    }

    & .row {
      & .column {
        display: flex;
        width: calc(100% / 7);

        & .coin {
          display: flex;
          align-items: center;
          justify-content: space-around;

          & img {
            width: 24px;
            height: 24px;
            margin-right: 5px;
          }
        }
      }
    }
  }
`
