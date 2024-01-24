import { useState } from "react";
import styled from "styled-components"

const TableWrapper = styled.div`
  height: calc(100vh - ${({top}) => top}px);
  overflow-y: scroll;
  width: 100%;

  &::-webkit-scrollbar {
    width: 5px;
  }


  &::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }
`;

const TableStyle = styled.table`
  width: 100%;

  & th {
    border: 1px solid white;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
  }

  & td {
    border: 1px solid white;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
  }
`;

const Table = ({ headers, data, buildRow }) => {
  const [ref, refState] = useState()

  return (
    <TableWrapper ref={ref => refState(ref)} top={ref?.getBoundingClientRect()?.top}>
      <TableStyle>
        <thead>
          <tr>
            {(headers || []).map((header) => (
              <th>{header.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {(data || []).map((row) => (
            <tr>
              {buildRow(row).map((field, index) => (
                <td key={index}>{field}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </TableStyle>
    </TableWrapper>
  )
}

export default Table
