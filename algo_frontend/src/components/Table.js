import styled from "styled-components"

const TableWrapper = styled.div`
  height: 300px;
  overflow-y: scroll;
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
  return (
    <TableWrapper>
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
