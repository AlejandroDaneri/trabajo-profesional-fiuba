import "../styles/graphsView.css";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  Rectangle,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import React, { PureComponent } from "react";

const generateTradingData = () => {
  const startDate = new Date(2023, 0, 1);
  const endDate = new Date(2023, 0, 10);
  const days = Math.floor((endDate - startDate) / (24 * 60 * 60 * 1000));

  const tradingData = [];

  for (let i = 0; i <= days; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);

    tradingData.push({
      date: date.toLocaleDateString(),
      open: Math.random() * 100 + 500,
      close: Math.random() * 100 + 500,
      high: Math.random() * 100 + 500,
      low: Math.random() * 100 + 500,
      volume: Math.floor(Math.random() * 100000),
    });
  }

  return tradingData;
};

const tradingChartData = generateTradingData();

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

export default class GraphsView extends PureComponent {
  render() {
    return (
      <div className="graphs-container">
        <div className="graph-item">
          <h3>Stock Price Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              width={500}
              height={300}
              data={tradingChartData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="close"
                stroke="#8884d8"
                activeDot={{ r: 8 }}
              />
              <Line type="monotone" dataKey="open" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="graph-item">
          <h3>Daily Stock Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              width={500}
              height={300}
              data={tradingChartData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar
                dataKey="close"
                fill="#8884d8"
                activeShape={<Rectangle fill="pink" stroke="blue" />}
              />
              <Bar
                dataKey="open"
                fill="#82ca9d"
                activeShape={<Rectangle fill="gold" stroke="purple" />}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="graph-item">
          <h3>Volume Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart width="100%" height="100%">
              <Pie
                data={tradingChartData}
                cx="50%"
                cy="50%"
                fill="#8884d8"
                dataKey="volume"
              >
                {tradingChartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
            <div className="pie-legend">
              {tradingChartData.map((entry, index) => (
                <div key={`legend-${index}`} className="legend-item">
                  <div
                    className="legend-color"
                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                  />
                  <div className="legend-label">{`${entry.date} - Volume: ${entry.volume}`}</div>
                </div>
              ))}
            </div>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }
}
