import styled from "styled-components"

export const ResultStyle = styled.div`
  color: ${({ win }) => (win ? "green" : "red")};
  font-weight: 600;
  width: 40px;
`

export const TradesStyle = styled.div`
  display: flex;
  flex-direction: column;
  height: 600px;
  align-items: center;
  width: 100%;

  & img {
    border-radius: 30px;
  }

  & p {
    color: white;
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
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
      border: 1px solid white;
      height: 40px;
      margin: 5px;
      border-radius: 10px;
      padding-left: 10px;
      padding-right: 10px;

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
