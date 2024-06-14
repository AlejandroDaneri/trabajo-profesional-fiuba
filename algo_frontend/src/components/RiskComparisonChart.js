import React from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts"
import styled from "styled-components"
import { theme } from "../utils/theme"

const ChartsStyle = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;

  & .risk {
    display: flex;
    flex-direction: column;
    width: 48%;

    & .chart {
      padding: 10px;
      background: linear-gradient(
        132.03deg,
        rgba(21, 24, 37, 0.4) 0%,
        rgba(11, 10, 7, 0.4) 100%
      );
    }
  }
`

const RiskComparisonChart = ({ risks, colors }) => {
  const data = Object.keys(risks).map((strategy, idx) => ({
    name: strategy,
    ...risks[strategy],
    fill: colors[idx] || "#2979FF",
  }))

  const yAxisTickFormatter = (value) => {
    if (value === "strategy") {
      return "Strategy"
    }
    return `Buy&Hold`
  }

  const risks_ = Object.keys(risks[Object.keys(risks)[0]]).map((risk) => ({
    label: risk
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase()),
    dataKey: risk,
  }))

  const calculateDomain = (dataKey) => {
    let min = Infinity
    let max = -Infinity
    data.forEach((d) => {
      if (Number(d[dataKey]) < min) min = Number(d[dataKey])
      if (Number(d[dataKey]) > max) max = Number(d[dataKey])
    })
    if (min > 0) min = 0
    if (max < 0) max = 0

    return [min, max]
  }

  return (
    <ChartsStyle>
      {risks_.map((risk, index) => (
        <div key={index} className="risk">
          <h4>{risk.label}</h4>
          <div className="chart">
            <ResponsiveContainer height={120}>
              <BarChart
                layout="vertical"
                data={data}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <YAxis
                  dataKey="name"
                  type="category"
                  tickFormatter={yAxisTickFormatter}
                  tick={{ fill: "#fff" }}
                />
                <XAxis
                  type="number"
                  domain={calculateDomain(risk.dataKey.value)}
                  tick={{ fill: "#fff" }}
                />
                <Tooltip content={risk.dataKey.description} />
                <Bar dataKey={risk.dataKey.value} fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      ))}
    </ChartsStyle>
  )
}

export default RiskComparisonChart
