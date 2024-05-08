/* Import Libs */
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
} from "recharts"
import { useEffect, useState } from "react"
import moment from 'moment'

/* Import Components */
import CurrencyLogo from "../components/CurrencyLogo"
import Trades from "../components/Trades"
import View from "../components/reusables/View"

/* Import Styled Components */
import { CurrentStrategyStyle } from "../styles/CurrentStrategy"

/* Import Utils */
import { capitalize } from "../utils/string"

/* Import WebApi */
import { get } from "../webapi/strategy"
import { get as getCandleticks } from "../webapi/candleticks"

/* Import Images */
import logoBinance from "../images/logos/exchanges/binance.svg"

/* Import Constants */
import { TIMEFRAMES } from "../constants"

const CurrentStrategy = () => {
  const [strategy, strategyFunc] = useState({
    loading: false,
    data: {
      currencies: [],
    },
  })

  const [candleticks, candleticksFunc] = useState({
    loading: false,
    data: []
  })

  //Here we should fetch the actual information from the database.
  const generateStockPerformanceData = () => {
    const startDate = new Date(2024, 2, 20)
    const endDate = new Date(2024, 4, 1)
    const weeks = Math.ceil((endDate - startDate) / (7 * 24 * 60 * 60 * 1000))

    const stockData = []

    for (let i = 0; i < weeks; i++) {
      const weekStartDate = new Date(startDate)
      weekStartDate.setDate(startDate.getDate() + i * 7)

      const weekEndDate = new Date(weekStartDate)
      weekEndDate.setDate(weekStartDate.getDate() + 6)

      const pv = Math.random() * 10000 - 5000
      const uv = Math.random() * 10000 - 5000

      stockData.push({
        name: `${weekStartDate.toLocaleDateString()} - ${weekEndDate.toLocaleDateString()}`,
        pv,
        uv,
      })
    }

    return stockData
  }

  //Here we should fetch the actual information from the database.
  const generateTradingData = () => {
    const startDate = new Date(2023, 0, 1)
    const endDate = new Date(2023, 0, 20)
    const days = Math.floor((endDate - startDate) / (24 * 60 * 60 * 1000))

    const tradingData = []

    for (let i = 0; i <= days; i++) {
      const date = new Date(startDate)
      date.setDate(startDate.getDate() + i)

      tradingData.push({
        date: date.toLocaleDateString(),
        strategy: Math.random() * 100 + 500,
        buyAndHold: Math.random() * 100 + 500,
      })
    }

    return tradingData
  }

  const tradingChartData = generateTradingData()

  const stockPerformanceChartData = generateStockPerformanceData()

  const getStrategy = () => {
    const transformToView = (data) => {
      const getDuration = (start) => {
        const end = Date.now() / 1000
        return moment.utc((end - start) * 1000).format('HH:mm:ss')
      }

      const transformTimeframe = (timeframe) => {
        return TIMEFRAMES.find(timeframe_ => timeframe_.value === timeframe)?.label
      }

      const initialBalance = data.initial_balance
      const currentBalance = parseFloat(data.current_balance).toFixed(2)
      const profitAndLoss = (currentBalance - initialBalance).toFixed(2)
      const profitAndLossPercentaje = (
        (currentBalance / initialBalance - 1) *
        100
      ).toFixed(2)
      const duration = getDuration(data.start_timestamp)

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
      }
    }
    strategyFunc((prevState) => ({
      ...prevState,
      loading: true,
    }))
    get()
      .then((response) => {
        strategyFunc((prevState) => ({
          ...prevState,
          loading: false,
          data: transformToView(response.data),
        }))
      })
      .catch((_) => {
      })
  }

  const getCandleticks_ = (symbol, start, end, timeframe) => {
    const params = {
      symbol,
      start,
      end,
      timeframe
    }

    getCandleticks(params)
      .then(response => {
        const amount = strategy.data.initial_balance / response.data[0].close

        candleticksFunc(prevState => ({
          ...prevState,
          loading: true,
          data: (response.data || []).map(candletick => {
            return {
              closeTime: new Date(candletick.close_time * 1000),
              close: (candletick.close  * amount).toFixed(2)
            }
          })
        }))
      })
      .catch(err => {
        console.info('err', err)
      })
  }

  useEffect(() => {
    if (strategy.data.currencies[0] && strategy.data.start_timestamp && strategy.data.timeframe) {
      getCandleticks_(
        strategy.data.currencies[0],
        strategy.data.start_timestamp,
        parseInt(Date.now() / 1000),
        strategy.data.timeframe.toLowerCase(),
      )
    }
  }, [
    strategy.data.currencies,
    strategy.data.start_timestamp,
    strategy.data.end_timestamp,
    strategy.data.timeframe
  ])

  useEffect(() => {
    const interval = setInterval(getStrategy, 10000)
    getStrategy()

    return () => {
      clearInterval(interval)
    }
  }, [])

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
                  {strategy.data.exchange === 'binance' && <img alt="Binance" src={logoBinance} width="24px" />}
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
            <div>
              <h3>Comparison of Strategies</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  width={500}
                  height={300}
                  data={candleticks.data}
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
                    dataKey="close"
                    stroke="#82ca9d"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            {false && <div className="graph-item">
              <h3>Weekly Stock Performance</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart
                  width={500}
                  height={300}
                  data={stockPerformanceChartData}
                  stackOffset="sign"
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
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
                  <ReferenceLine y={0} stroke="#000" />
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
            </div>}
          </div>
        </CurrentStrategyStyle>
      }
    />
  )
}

export default CurrentStrategy
