import React, { useState } from "react"
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Brush,
  Area,
  AreaChart,
} from "recharts"
import styled from "styled-components"

import FieldSwitch from "./FieldSwitch"

const ChartStyle = styled.div`
  & .field {
    margin-bottom: 10px;
  }
`

const StrategyComparisonChart = ({ data, colors, logScaleDefault, hideBrush }) => {
  const [logScale, setLogScale] = useState(logScaleDefault)
  const [zoomedData, setZoomedData] = useState(data)

  const toggleLogScale = () => {
    setLogScale((prevLogScale) => !prevLogScale)
  }

  const handleBrushChange = (domain) => {
    if (domain && domain.length === 2) {
      const [start, end] = domain
      const newData = data.filter(
        (entry) => entry.date >= start && entry.date <= end
      )
      setZoomedData(newData)
    } else {
      setZoomedData(data)
    }
  }

  return (
    <ChartStyle>
      <div className="field">
        <FieldSwitch
          id="log_scale"
          name="log_scale"
          label="Log Scale"
          value={logScale}
          onChange={toggleLogScale}
        />
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          {logScale ? (
            <YAxis
              label={{ value: "Balance", position: "insideLeft" }}
              scale={logScale && "log"}
              domain={logScale && ["auto", "auto"]}
            />
          ) : (
            <YAxis label={{ value: "Balance", position: "insideLeft" }} />
          )}

          <Tooltip />
          <Legend />
          <Area
            type="monotone"
            dataKey="balance_buy_and_hold"
            name="Balance Buy and Hold"
            stroke={colors[0]}
            fill={colors[0]}
            connectNulls
          />
          <Area
            type="monotone"
            dataKey="balance_strategy"
            name="Balance Strategy"
            stroke={colors[1]}
            fill={colors[1]}
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="balance_buy_and_hold"
            stroke={colors[0]}
            dot={false}
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="balance_strategy"
            stroke={colors[1]}
            dot={false}
            connectNulls
          />
          {!hideBrush && <Brush dataKey="date" onChange={handleBrushChange}>
            <AreaChart>
              <Area
                type="monotone"
                dataKey="balance_buy_and_hold"
                stroke={colors[0]}
                fill={colors[0]}
                connectNulls
              />
              <Area
                type="monotone"
                dataKey="balance_strategy"
                stroke={colors[1]}
                fill={colors[1]}
                connectNulls
              />
            </AreaChart>
          </Brush>}
        </LineChart>
      </ResponsiveContainer>
    </ChartStyle>
  )
}

export default StrategyComparisonChart
