/* Import Libs */
import React, { useState } from "react"
import {
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
import { format } from "date-fns"
/* Import Reusable Components */
import FieldSwitch from "./FieldSwitch"

import { theme } from "../../utils/theme"

const ChartStyle = styled.div`
  display: flex;
  flex-direction: column;
  border-radius: 4px;
  padding: 10px;
  background: linear-gradient(
    132.03deg,
    rgba(21, 24, 37, 0.4) 0%,
    rgba(11, 10, 7, 0.4) 100%
  );

  & .field {
    margin-bottom: 10px;
  }
`

const StrategyComparisonChart = ({
  data,
  colors,
  logScaleDefault,
  hideBrush,
  height,
}) => {
  const [logScale, setLogScale] = useState(logScaleDefault)
  const [zoomedData, setZoomedData] = useState(data)

  const toggleLogScale = () => {
    setLogScale((prevLogScale) => !prevLogScale)
  }
  const dateFormatter = (tick) => format(new Date(tick), "yyyy-MM-dd")
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
      <ResponsiveContainer height={height || 400}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 20 }}
        >
          <XAxis
            dataKey="date"
            angle={-20}
            textAnchor="end"
            height={70}
            tickFormatter={dateFormatter}
          />
          {logScale ? (
            <YAxis
              label={{
                value: "Balance",
                angle: -90,
                position: "insideLeft",
                offset: -10,
              }}
              scale={logScale && "log"}
              domain={logScale && ["auto", "auto"]}
            />
          ) : (
            <YAxis
              label={{
                value: "Balance",
                angle: -90,
                position: "insideLeft",
                offset: -10,
              }}
            />
          )}
          <Tooltip contentStyle={{ backgroundColor: theme.black }} />
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
          {!hideBrush && (
            <Brush dataKey="date" onChange={handleBrushChange}>
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
            </Brush>
          )}
        </LineChart>
      </ResponsiveContainer>
    </ChartStyle>
  )
}

export default StrategyComparisonChart
