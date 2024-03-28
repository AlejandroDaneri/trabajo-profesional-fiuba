import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useEffect, useState } from "react";

import CurrencyLogo from "../components/CurrencyLogo";
import { CurrentStrategyStyle } from "../styles/CurrentStrategy";
import Trades from "../components/Trades";
import View from "../components/reusables/View";
import { capitalize } from "../utils/string";
import { get } from "../webapi/strategy";

const CurrentStrategy = () => {
  const [strategy, strategyFunc] = useState({
    loading: true,
    data: {
      currencies: [],
    },
  });

  //Here we should fetch the actual information from the database.
  const generateTradingData = () => {
    const startDate = new Date(2023, 0, 1);
    const endDate = new Date(2023, 0, 20);
    const days = Math.floor((endDate - startDate) / (24 * 60 * 60 * 1000));

    const tradingData = [];

    for (let i = 0; i <= days; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);

      tradingData.push({
        date: date.toLocaleDateString(),
        strategy: Math.random() * 100 + 500,
        buyAndHold: Math.random() * 100 + 500,
      });
    }

    return tradingData;
  };

  const tradingChartData = generateTradingData();

  const getStrategy = () => {
    const transformToView = (data) => {
      const transformDuration = (start) => {
        const currentTime = Math.floor(Date.now() / 1000);

        const durationInSeconds = currentTime - start;

        const days = Math.floor(durationInSeconds / (3600 * 24));
        const hours = Math.floor((durationInSeconds % (3600 * 24)) / 3600);

        return `${days} days, ${hours} hours`;
      };

      const transformTimeframe = (timeframe) => {
        switch (timeframe) {
          case "1M":
            return "1 minute";
          case "1H":
            return "1 hour";
          default:
            return "";
        }
      };

      const initialBalance = data.initial_balance;
      const currentBalance = parseFloat(data.current_balance).toFixed(2);
      const profitAndLoss = (currentBalance - initialBalance).toFixed(2);
      const profitAndLossPercentaje = (
        (currentBalance / initialBalance - 1) *
        100
      ).toFixed(2);
      const duration = transformDuration(data.start_timestamp);
      const timeframe = transformTimeframe(data.timeframe);

      return {
        ...data,
        current_balance: parseFloat(data.current_balance).toFixed(2),
        profit_and_loss_label: `${profitAndLoss} (${profitAndLossPercentaje}%)`,
        indicators: (data.indicators || []).map((indicator) => ({
          ...indicator,
          name: (() => {
            switch (indicator.name) {
              case "rsi":
                return "RSI";
              default:
                return capitalize(indicator.name);
            }
          })(),
          parameters: Object.keys(indicator.parameters).map((key) => ({
            key: key
              .split("_")
              .map((word) => capitalize(word))
              .join(" "),
            value: indicator.parameters[key],
          })),
        })),
        duration,
        timeframe,
      };
    };
    get()
      .then((response) => {
        strategyFunc((prevState) => ({
          ...prevState,
          loading: false,
          data: transformToView(response.data),
        }));
      })
      .catch((_) => {});
  };

  useEffect(() => {
    getStrategy();
  }, []);

  return (
    <View
      title="Current Strategy"
      content={
        <CurrentStrategyStyle>
          <div className="summary">
            <h2>Summary</h2>
            <div className="summary-content">
              <div className="box">
                <div className="label">Initial Balance</div>
                <div className="value">{strategy.data.initial_balance}</div>
              </div>
              <div className="box">
                <div className="label">Current Balance</div>
                <div className="value">{strategy.data.current_balance}</div>
              </div>
              <div className="box">
                <div className="label">Profit/Loss</div>
                <div className="value">
                  {strategy.data.profit_and_loss_label}
                </div>
              </div>
              <div className="box">
                <div className="label">Currencies</div>
                <div className="value">
                  {strategy.data.currencies.map((currency) => (
                    <div className="currency-wrapper">
                      <CurrencyLogo currency={currency} />
                    </div>
                  ))}
                </div>
              </div>
              <div className="box">
                <div className="label">Duration</div>
                <div>{strategy.data.duration}</div>
              </div>
              <div className="box">
                <div className="label">Timeframe</div>
                <div>{strategy.data.timeframe}</div>
              </div>
            </div>
          </div>
          <div className="trades">
            <h2>Trades</h2>
            <Trades strategyID={strategy.data.id} />
          </div>
          <div>
            <h2>Graphs</h2>
            <div className="graph-item">
              <h3>Comparison of Strategies</h3>
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
                  <YAxis
                    label={{
                      value: "Balance",
                      angle: -90,
                      position: "insideLeft",
                    }}
                  />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="strategy"
                    name="Current Strategy"
                    stroke="#8884d8"
                    activeDot={{ r: 8 }}
                  />
                  <Line
                    type="monotone"
                    name="Buy And Hold"
                    dataKey="buyAndHold"
                    stroke="#82ca9d"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </CurrentStrategyStyle>
      }
    />
  );
};

export default CurrentStrategy;
