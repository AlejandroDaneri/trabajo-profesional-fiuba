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

  & span {
    color: white;
  }

  & thead {
    display: table;
    width: 100%;

    & th {
      width: calc(100% / ${({ columns }) => columns});
    }
  }

  & tbody {
    display: table;
    width: 100%;

    & td {
      width: calc(100% / ${({ columns }) => columns});
    }
  }

  & th {
    border: 1px solid white;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
  }

  & td {
    border: 0.5px solid white;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
  }
`;

const ThContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: ${({ clickeable }) => clickeable && 'pointer'};
` 

const Table = ({ headers, data, buildRow }) => {
  const [ref, refState] = useState()

  const [sort, sortFunc] = useState({
    field: 'amount',
    direction: 'asc' 
  })

  const onSort = (field) => {
    if (field) {
      sortFunc(prevState => ({
        ...prevState,
        field,
        direction: prevState.direction === 'asc' ? 'desc' : 'asc'
      }))
    }
  }

  const sort_ = (list, key, direction) => {
    if (direction === 'asc') {
      return list.sort((a, b) => a[key] - b[key])
    }
    if (direction === 'desc') {
      return list.sort((a, b) => b[key] - a[key])
    }
  }

  const dataSorted = sort_(data, sort.field, sort.direction)

  return (
    <TableWrapper
      ref={ref => refState(ref)}
      top={ref?.getBoundingClientRect()?.top}
    >
      <TableStyle columns={headers.length}>
        <thead>
          <tr>
            {(headers || []).map((header) => (
              <th>
                <ThContainer clickeable={header.sortable} onClick={() => onSort(header.value)}>
                  {header.label}
                  {(sort.field === header.value) && <span className="material-icons">{sort.direction === 'asc' ? 'arrow_drop_up' : 'arrow_drop_down'}</span>}
                </ThContainer>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {(dataSorted || []).map((row) => (
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
