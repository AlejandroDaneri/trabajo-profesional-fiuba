import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import styled from "styled-components";

const ChartContainer = styled.div`
  width: 100%;
  display: flex;
  flex-wrap: wrap;
`;

const RiskComparisonChart = ({ risks }) => {
  // Convertir los datos de riesgos en un array de objetos para usar con Recharts
  const data = Object.keys(risks).map((strategy, idx) => ({
    name: strategy,
    ...risks[strategy],
    fill: idx === 0 ? "#00C853" : "#2979FF",
  }));

  // Lista de pares de riesgos a comparar
  const riskPairs = [
    { label: "Kelly Criterion", dataKey: "kelly_criterion" },
    { label: "Max Drawdown", dataKey: "max_drawdown" },
    { label: "Payoff Ratio", dataKey: "payoff_ratio" },
    { label: "Rachev Ratio", dataKey: "rachev_ratio" },
  ];

  // Renderizar los gráficos para cada par de riesgos
  const renderCharts = () => {
    return riskPairs.map((pair, index) => (
      <div key={index} style={{ width: "50%" }}>
        <h3>{pair.label}</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            layout="vertical"
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <YAxis dataKey="name" type="category" />
            <XAxis type="number" />
            <Tooltip />
            <Legend />
            <Bar dataKey={pair.dataKey} fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    ));
  };

  // Renderizar el componente
  return <ChartContainer>{renderCharts()}</ChartContainer>;
};

export default RiskComparisonChart;
