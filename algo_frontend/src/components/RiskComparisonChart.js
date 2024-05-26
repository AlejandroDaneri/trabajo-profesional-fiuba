import React from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import styled from "styled-components"

const ChartContainer = styled.div`
  width: 100%;
  display: flex;
  flex-wrap: wrap;
`

const RiskComparisonChart = ({ risks, colors }) => {
  const data = Object.keys(risks).map((strategy, idx) => ({
    name: strategy,
    ...risks[strategy],
    fill: colors[idx] || "#2979FF",
  }))
  const yAxisTickFormatter = (value) => {
    if (value == "strategy") {
      return "Strategy"
    }
    return `B&H`
  }
  const riskPairs = [
    { label: "Kelly Criterion", dataKey: "kelly_criterion" },
    { label: "Max Drawdown", dataKey: "max_drawdown" },
    { label: "Payoff Ratio", dataKey: "payoff_ratio" },
    { label: "Rachev Ratio", dataKey: "rachev_ratio" },
  ]

  const renderCharts = () => {
    return riskPairs.map((pair, index) => (
      <div key={index} style={{ width: "50%" }}>
        <h4>{pair.label}</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            layout="vertical"
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <YAxis
              dataKey="name"
              type="category"
              tickFormatter={yAxisTickFormatter}
            />
            <XAxis type="number" />
            <Tooltip />
            <Bar dataKey={pair.dataKey} fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    ))
  }

  return <ChartContainer>{renderCharts()}</ChartContainer>
}

export default RiskComparisonChart
