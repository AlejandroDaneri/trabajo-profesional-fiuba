import styled from "styled-components"

const TableStyle = styled.table`
  & th {
    border: 1px solid white;
    text-align: center;
  }
  & td {
    border: 1px solid white;
    text-align: center;
  }
`

const Table = ({ headers, data, buildRow }) => {
  return (
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
  )
}

export default Table
