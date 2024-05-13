/* Import Libs */
import { useState } from "react"
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import styled from "styled-components"

/* Import Reusables Components */
import FieldSwitch from "./FieldSwitch"

const ChartStyle = styled.div`
  & .field {
    margin-bottom: 10px;
  }
`
const Chart = ({ data, colors }) => {
  const [logScale, logScaleFunc] = useState(false)

  const onToggle = () => {
    logScaleFunc((prevState) => !prevState)
  }

  return (
    <ChartStyle>
      <div className="field">
        <FieldSwitch
          id="log_scale"
          name="log_scale"
          label="Log Scale"
          value={logScale}
          onChange={onToggle}
        />
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />

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

          <Line
            type="monotone"
            dataKey="balance_buy_and_hold"
            name="Balance Buy and Hold"
            stroke={colors[0]} // Cambiar el color de la línea Buy and Hold
            activeDot={{ r: 8 }}
            dot={false}
          />

          <Line
            type="monotone"
            dataKey="balance_strategy"
            name="Balance Strategy"
            stroke={colors[1]} // Cambiar el color de la línea Strategy
            activeDot={{ r: 8 }}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartStyle>
  )
}

export default Chart
