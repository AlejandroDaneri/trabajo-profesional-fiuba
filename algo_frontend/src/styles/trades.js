import styled from "styled-components"

export const TypeStyle = styled.div`
  color: ${({ type }) => (type === "SELL" ? "red" : "green")};
  font-weight: 600;
  width: 40px;
`

export const TradesStyle = styled.div`
  display: flex;
  flex-direction: column;
  height: 600px;

  & img {
    border-radius: 30px;
  }

  & p {
    color: white;
  }

  .trades::-webkit-scrollbar {
    width: 5px;
  }

  .trades::-webkit-scrollbar-track {
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  }

  .trades::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }

  & .trades {
    overflow-y: scroll;
  }

  & .trade {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    border: 1px solid white;
    width: 800px;
    height: 40px;
    margin: 5px;
    border-radius: 10px;
    padding-left: 10px;
    padding-right: 10px;

    & .timestamp {
      width: 160px;
    }

    & .type {
      color: green;
    }

    & .type {
      color: red;
    }

    & .coin {
      display: flex;
      align-items: center;
      width: 60px;
      justify-content: space-around;

      & img {
        width: 24px;
        height: 24px;
      }
    }

    & .price {
      width: 60px;
    }

    & .amount {
      width: 200px;
    }
  }
`
