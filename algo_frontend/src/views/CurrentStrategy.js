import "react-datepicker/dist/react-datepicker.css";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useEffect, useState } from "react";

import CurrencyLogo from "../components/CurrencyLogo";
import { CurrentStrategyStyle } from "../styles/CurrentStrategy";
import DatePicker from "react-datepicker";
import Trades from "../components/Trades";
import View from "../components/reusables/View";
import { capitalize } from "../utils/string";
import { get } from "../webapi/strategy";
import { get as getCandleticks } from "../webapi/candleticks";
import logoBinance from "../images/logos/exchanges/binance.svg";
import moment from "moment";

const CurrentStrategy = () => {
  const [strategy, strategyFunc] = useState({
    loading: false,
    data: {
      currencies: [],
    },
  });

  const [candleticks, candleticksFunc] = useState({
    loading: false,
    data: [],
  });

  const [minSelectedDate, setMinSelectedDate] = useState(new Date(2024, 0, 1));
  const [maxSelectedDate, setMaxSelectedDate] = useState(new Date());

  //Here we should fetch the actual information from the database.
  const generateStockPerformanceData = () => {
    const startDate = new Date(2024, 0, 1);
    const endDate = new Date(2024, 0, 20);
    const weeks = Math.ceil((endDate - startDate) / (7 * 24 * 60 * 60 * 1000));

    const stockData = [];

    for (let i = 0; i < weeks; i++) {
      const weekStartDate = new Date(startDate);
      weekStartDate.setDate(startDate.getDate() + i * 7);

      const weekEndDate = new Date(weekStartDate);
      weekEndDate.setDate(weekStartDate.getDate() + 6);

      const pv = Math.random() * 10000 - 5000;
      const uv = Math.random() * 10000 - 5000;

      stockData.push({
        name: `${weekStartDate.toLocaleDateString()} - ${weekEndDate.toLocaleDateString()}`,
        startDate: weekStartDate,
        pv,
        uv,
      });
    }

    return stockData;
  };

  //Here we should fetch the actual information from the database.
  const generateTradingData = () => {
    const startDate = new Date(2024, 0, 1);
    const endDate = new Date(2024, 0, 20);
    const days = Math.floor((endDate - startDate) / (24 * 60 * 60 * 1000));

    const tradingData = [];

    for (let i = 0; i <= days; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);

      tradingData.push({
        date: date,
        strategy: (Math.random() * 100 + 500).toFixed(1),
        buyAndHold: (Math.random() * 100 + 500).toFixed(1),
      });
    }

    return tradingData;
  };

  const tradingChartData = generateTradingData();

  const stockPerformanceChartData = generateStockPerformanceData();

  const filteredStockPerformanceData = stockPerformanceChartData
    .filter(
      (item) =>
        item.startDate >= minSelectedDate && item.startDate <= maxSelectedDate
    )
    .map((entry) => ({
      ...entry,
    }));

  const filteredTradingChartData = tradingChartData
    .filter(
      (item) => item.date >= minSelectedDate && item.date <= maxSelectedDate
    )
    .map((entry) => ({
      ...entry,
      date: entry.date.toLocaleDateString(),
    }));

  const getStrategy = () => {
    const transformToView = (data) => {
      const getDuration = (start) => {
        const end = Date.now() / 1000;
        return moment.utc((end - start) * 1000).format("HH:mm:ss");
      };

      const transformTimeframe = (timeframe) => {
        switch (timeframe) {
          case "1M":
            return "1 minute";
          case "5M":
            return "5 minute";
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
      const duration = getDuration(data.start_timestamp);

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
        timeframe_label: transformTimeframe(data.timeframe),
      };
    };
    strategyFunc((prevState) => ({
      ...prevState,
      loading: true,
    }));
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

  const getCandleticks_ = (symbol, start, end, timeframe) => {
    const params = {
      symbol,
      start,
      end,
      timeframe,
    };

    getCandleticks(params)
      .then((response) => {
        const amount = strategy.data.initial_balance / response.data[0].close;

        candleticksFunc((prevState) => ({
          ...prevState,
          loading: true,
          data: (response.data || []).map((candletick) => {
            return {
              closeTime: new Date(candletick.close_time * 1000),
              close: (candletick.close * amount).toFixed(2),
            };
          }),
        }));
      })
      .catch((err) => {
        console.info("err", err);
      });
  };

  useEffect(() => {
    if (
      strategy.data.currencies[0] &&
      strategy.data.start_timestamp &&
      strategy.data.timeframe
    ) {
      getCandleticks_(
        strategy.data.currencies[0],
        strategy.data.start_timestamp,
        parseInt(Date.now() / 1000),
        strategy.data.timeframe.toLowerCase()
      );
    }
  }, [
    strategy.data.currencies,
    strategy.data.start_timestamp,
    strategy.data.end_timestamp,
    strategy.data.timeframe,
  ]);

  useEffect(() => {
    const interval = setInterval(getStrategy, 10000);
    getStrategy();

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <View
      title="Running Strategy"
      loading={strategy.loading}
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
                <div className="label">Exchange</div>
                <div className="value">
                  {strategy.data.exchange === "binance" && (
                    <img alt="Binance" src={logoBinance} width="24px" />
                  )}
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
                <div>{strategy.data.timeframe_label}</div>
              </div>
            </div>
          </div>
          <div className="trades">
            <h2>Trades</h2>
            <Trades strategyID={strategy.data.id} />
          </div>
          <div>
            <h2>Graphs</h2>
            <div style={{ display: "flex", justifyContent: "center" }}>
              <div style={{ marginRight: "10px" }}>
                <label
                  style={{ marginRight: "10px" }}
                  htmlFor="startDatePicker"
                >
                  Select the start date:
                </label>
                <DatePicker
                  id="startDatePicker"
                  selected={minSelectedDate}
                  onChange={(date) => setMinSelectedDate(date)}
                  className="input-strategy"
                />
              </div>
              <div>
                <label style={{ marginRight: "10px" }} htmlFor="endDatePicker">
                  Select the end date:
                </label>
                <DatePicker
                  id="endDatePicker"
                  selected={maxSelectedDate}
                  onChange={(date) => setMaxSelectedDate(date)}
                  className="input-strategy"
                />
              </div>
            </div>
            <div>
              <h3>Comparison of Strategies</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  width={500}
                  height={300}
                  data={filteredTradingChartData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid stroke="none" strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis
                    label={{
                      value: "Balance",
                      angle: -90,
                      position: "insideLeft",
                    }}
                    domain={[
                      Math.min(
                        ...tradingChartData.map((item) => item.strategy)
                      ),
                      Math.max(
                        ...tradingChartData.map((item) => item.strategy)
                      ),
                    ]}
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
                    dataKey="close"
                    stroke="#82ca9d"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            {false && (
              <div className="graph-item">
                <h3>Weekly Stock Performance</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    width={500}
                    height={300}
                    data={filteredStockPerformanceData}
                    stackOffset="sign"
                    margin={{
                      top: 5,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid stroke="none" strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis
                      label={{
                        value: "Profit/Loss",
                        angle: -90,
                        position: "insideLeft",
                        style: { textAnchor: "middle" },
                      }}
                    />
                    <Tooltip />
                    <Legend />
                    <ReferenceLine y={0} stroke="#484a4d" />
                    <Bar
                      dataKey="pv"
                      name="Current Strategy"
                      fill="#8884d8"
                      stackId="stack"
                    />
                    <Bar
                      dataKey="uv"
                      name="Buy and Hold"
                      fill="#82ca9d"
                      stackId="stack"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </CurrentStrategyStyle>
      }
    />
  );
};

export default CurrentStrategy;
