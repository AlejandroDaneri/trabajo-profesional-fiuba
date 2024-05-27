import React from "react"
import styled from "styled-components"

const TradesTable = ({ trades }) => {
  const formatNumber = (num) => num.toFixed(2)
  const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 1em;
    font-family: "Arial, sans-serif";
    min-width: 400px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
  `

  const THead = styled.thead`
    tr {
      background-color: #c2c2c2;
      color: #202020;
      text-align: left;
    }
  `

  const TBody = styled.tbody`
    tr {
      border-bottom: 1px solid #dddddd;
    }

    tr:nth-of-type(even) {
      background-color: #131313;
    }
  `

  const TD = styled.td`
    padding: 12px 15px;
    border: 1px solid #ddd;
  `

  return (
    <Table>
      <THead>
        <tr>
          <th>Entry Date</th>
          <th>Entry Price (US$)</th>
          <th>Output Date</th>
          <th>Output Price (US$)</th>
          <th>Trade Duration (days)</th>
          <th>Commission (US$)</th>
          <th>Return (%)</th>
          {/* <th>Cumulative Return (%)</th> */}
          <th>Result</th>
        </tr>
      </THead>
      <TBody>
        {trades.map((trade, index) => {
          const entryDate = new Date(trade.entry_date)
          const outputDate = new Date(trade.output_date)
          const tradeDurationDays = Math.ceil(
            (outputDate - entryDate) / (1000 * 60 * 60 * 24) // Convertir diferencia en milisegundos a días
          )

          return (
            <tr key={index}>
              <TD>{trade.entry_date}</TD>
              <TD>{formatNumber(trade.entry_price)}</TD>
              <TD>{trade.output_date}</TD>
              <TD>{formatNumber(trade.output_price)}</TD>
              <TD>{tradeDurationDays}</TD>

              <TD>
                {formatNumber(
                  trade.fixed_commission + trade.variable_commission
                )}
              </TD>
              <TD>{formatNumber(trade.return)}</TD>
              {/* <TD>{formatNumber(trade.cumulative_return)}</TD> */}
              <TD>{trade.result}</TD>
            </tr>
          )
        })}
      </TBody>
    </Table>
  )
}

export default TradesTable
