import React, { useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"

const allData = {
  "1d": [{ date: "5/25", OIWeighted: 8, VolWeighted: 7 }],
  "1w": [
    { date: "5/19", OIWeighted: 7, VolWeighted: 6 },
    { date: "5/20", OIWeighted: 8, VolWeighted: 9 },
    { date: "5/21", OIWeighted: 10, VolWeighted: 11 },
    { date: "5/21", OIWeighted: 12, VolWeighted: 14 },
    { date: "5/22", OIWeighted: 9, VolWeighted: 10 },
    { date: "5/23", OIWeighted: 13, VolWeighted: 12 },
    { date: "5/24", OIWeighted: 10, VolWeighted: 9 },
    { date: "5/25", OIWeighted: 8, VolWeighted: 7 },
  ],
  "1m": [
    // Suponiendo que los datos de un mes están aquí
  ],
  "3m": [
    // Suponiendo que los datos de tres meses están aquí
  ],
  // Agregar más datos para otros intervalos de tiempo según sea necesario
}

const ChartComponent = () => {
  const [timeframe, setTimeframe] = useState("1w")

  const handleTimeframeChange = (event) => {
    setTimeframe(event.target.value)
  }

  return (
    <div style={styles.chartContainer}>
      <div style={styles.selectorContainer}>
        <select
          value={timeframe}
          onChange={handleTimeframeChange}
          style={styles.selector}
        >
          <option value="1d">1d</option>
          <option value="1w">1w</option>
          <option value="1m">1m</option>
          <option value="3m">3m</option>
          <option value="6m">6m</option>
          <option value="1y">1y</option>
          <option value="3y">3y</option>
        </select>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={allData[timeframe]}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="date" tick={{ fill: "white" }} />
          <YAxis tick={{ fill: "white" }} />
          <Tooltip
            contentStyle={{ backgroundColor: "#1e1e2f", border: "none" }}
            itemStyle={{ color: "white" }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="OIWeighted"
            stroke="#3b82f6"
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="VolWeighted"
            stroke="#8b5cf6"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

const styles = {
  chartContainer: {
    width: "800px",
    height: "400px",
    backgroundColor: "#1e1e2f",
    padding: "20px",
    borderRadius: "8px",
  },
  selectorContainer: {
    display: "flex",
    justifyContent: "flex-end",
    marginBottom: "10px",
  },
  selector: {
    backgroundColor: "#1e1e2f",
    color: "white",
    border: "1px solid #3b82f6",
    borderRadius: "4px",
    padding: "5px",
  },
}

export default ChartComponent
