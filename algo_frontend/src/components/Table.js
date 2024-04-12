import styled, { css } from "styled-components"
import { useState } from "react"

const TableWrapper = styled.div`
  max-height: calc(100vh - ${({ top }) => top}px);
  overflow-y: scroll;
  width: 100%;

  &::-webkit-scrollbar {
    width: 5px;
  }

  &::-webkit-scrollbar-thumb {
    background-color: darkgrey;
    outline: 1px solid slategrey;
  }
`

const TableStyle = styled.table`
  width: 100%;

  & span {
    color: white;
  }

  & thead {
    display: table;
    width: 100%;

    & th {
      ${({ columnsWidth }) =>
        (columnsWidth || []).map((column, index) => {
          return css`
            &:nth-child(${index + 1}) {
              width: calc(${column}%);
            }
          `
        })}
    }
  }

  & tbody {
    display: table;
    width: 100%;

    & td {
      ${({ columnsWidth }) =>
        (columnsWidth || []).map((column, index) => {
          return css`
            &:nth-child(${index + 1}) {
              width: calc(${column}%);
            }
          `
        })}
    }
  }

  & th {
    border: 1px solid white;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
    height: 35px;
  }

  & td {
    border: 0.5px solid white;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
    height: 35px;
  }
`

const ThContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: ${({ clickeable }) => clickeable && "pointer"};
`

const Table = ({ headers, data, buildRow }) => {
  const [ref, refState] = useState()

  const [sort, sortFunc] = useState({
    field: headers.find((header) => header.default).value,
    direction: "desc",
  })

  const onSort = (field) => {
    if (field) {
      sortFunc((prevState) => ({
        ...prevState,
        field,
        direction: prevState.direction === "asc" ? "desc" : "asc",
      }))
    }
  }

  const sort_ = (list, key, direction) => {
    if (list != null) {
      if (direction === "asc") {
        return list.sort((a, b) => a[key] - b[key])
      }
      if (direction === "desc") {
        return list.sort((a, b) => b[key] - a[key])
      }
    }
  }

  const dataSorted = sort_(data, sort.field, sort.direction)

  const totalRemanent =
    100 -
    (headers || [])
      .map((header) => (header.width ? header.width : 0))
      .reduce((a, b) => a + b, 0)
  const countRemanent =
    (headers || []).length -
    (headers || [])
      .map((header) => (header.width ? 1 : 0))
      .reduce((a, b) => a + b, 0)
  const columnsWidth = (headers || []).map((header) =>
    header.width ? header.width : totalRemanent / countRemanent
  )

  return (
    <TableWrapper
      ref={(ref) => refState(ref)}
      top={ref?.getBoundingClientRect()?.top}
    >
      <TableStyle columns={headers.length} columnsWidth={columnsWidth}>
        <thead>
          <tr>
            {(headers || []).map((header) => (
              <th>
                <ThContainer
                  clickeable={header.sortable}
                  onClick={() => onSort(header.value)}
                >
                  {header.label}
                  {sort.field === header.value && (
                    <span className="material-icons">
                      {sort.direction === "asc"
                        ? "arrow_drop_up"
                        : "arrow_drop_down"}
                    </span>
                  )}
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
