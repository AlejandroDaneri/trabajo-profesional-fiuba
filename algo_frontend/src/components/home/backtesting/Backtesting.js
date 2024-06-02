/* Import Libs */
import React, { useEffect, useState } from "react"
import styled from "styled-components"
import BounceLoader from "react-spinners/BounceLoader"
import { useDispatch } from "react-redux"
import "react-day-picker/dist/style.css"

/* Import Reusables Components */
import View from "../../reusables/View"
import FieldInput from "../../reusables/FieldInput"
import FieldSelect from "../../reusables/FieldSelect"
import FieldSwitch from "../../reusables/FieldSwitch"
import FieldDatePicker from "../../reusables/FieldDatePicker"
import Box from "../../reusables/Box"
import Button from "../../Button"
import StrategyComparisonChart from "../../reusables/Chart"
import RiskComparisonChart from "../../RiskComparisonChart"
import { POPUP_ACTION_OPEN, POPUP_TYPE_ERROR } from "../../Popup"
import Table from "../../Table"

/* Impor WebApi */
import {
  getIndicators,
  run as runBacktesting,
} from "../../../webapi/backtesting"

/* Import Utils */
import { theme } from "../../../utils/theme"
import { capitalize } from "../../../utils/string"

/* Import Constants */
import {
  CRYPTOCURRENCIES,
  TIMEFRAMES,
  BACKTESTING_TYPES,
  STRATEGIES_TYPES,
} from "../../../constants"

const VIEW_FORM = 0
const VIEW_BACKTESTING = 1
const formatNumber = (num) => num.toFixed(2)

const headers = [
  {
    value: "buy_timestamp",
    label: "Date Buy",
    sortable: true,
    default: true,
    direction: "desc",
  },
  {
    value: "sell_timestamp",
    label: "Date Sell",
    sortable: true,
  },
  {
    value: "duration",
    label: "Duration (days)",
    sortable: true,
  },
  {
    value: "buy_price",
    label: "Price Buy ($)",
    sortable: true,
  },
  {
    value: "sell_price",
    label: "Price Sell ($)",
    sortable: true,
  },
  {
    value: "comission",
    label: "Comission",
    sortable: false,
  },
  {
    value: "return",
    label: "Return",
    sortable: true,
  },
  {
    value: "result",
    label: "Result",
    sortable: true,
  },
]

const buildRow = (trade) => {
  return [
    trade.entry_date,
    trade.output_date,
    (new Date(trade.output_date) - new Date(trade.entry_date)) /
      (1000 * 60 * 60 * 24),
    formatNumber(trade.entry_price),
    formatNumber(trade.output_price),
    formatNumber(trade.fixed_commission + trade.variable_commission),
    formatNumber(trade.return),
    trade.result,
  ]
}
const TradesTableDiv = styled.div`
  display: flex;
  width: 100%;
  max-height: 1000px;
  min-height: 200px;
`

const BacktestingStyle = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
  overflow: hidden;
  height: calc(100vh - 40px - 84px);

  & .divider {
    width: 2px;
    background: white;
    z-index: 2;
  }

  & .button-back {
    position: relative;
    right: 16px;
    top: 20px;
    z-index: 2;
  }

  & .backtesting {
    display: flex;
    justify-content: center;
    align-items: center;
  }
`

const BacktestingOutputStyle = styled.div`
  display: flex;
  width: calc(100% - ${({ show }) => (!show ? "600px" : "10px")});
  padding: 20px;
  flex-direction: column;
  height: calc(100vh - 40px - 84px);
  overflow-y: auto;

  & .chart-container {
    & h3 {
      border-bottom: 1px solid white;
      padding-bottom: 5px;
    }
  }

  & .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  & .boxes {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 20px;

    & .box {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 50px;
      border: 1px solid white;
      padding: 10px;
      border-radius: 4px;
      flex-grow: 1;
      margin-right: 20px;

      & .label {
        color: #a5a8b6;
        text-align: center;
      }

      & .value {
        display: flex;
        font-weight: 800;
        justify-content: center;

        & .currency-wrapper {
          margin-right: 5px;
        }
      }
    }
  }
`

const BacktestingFormStyle = styled.div`
  display: flex;
  flex-direction: column;
  padding-left: 20px;
  padding-top: 20px;
  padding-right: 20px;
  background: ${theme.dark};
  width: ${({ show }) => (show ? "600px" : "10px")};
  overflow-y: auto;
  transition: width 0.5s;

  & .sections {
    display: flex;
    flex-direction: column;
    z-index: ${({ show }) => (show ? "5" : "-1")};

    & .section {
      margin-bottom: 20px;

      & h3 {
        border-bottom: 0.5px solid white;
        padding-bottom: 5px;
        margin-bottom: 10px;
      }

      & .section-content.row {
        flex-direction: row;
      }

      & .section-content {
        display: flex;
        flex-direction: column;

        & .indicators {
          height: 300px;
          overflow-y: scroll;

          & .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
          }

          &::-webkit-scrollbar {
            -webkit-appearance: none;
            width: 8px;
          }

          &::-webkit-scrollbar-thumb {
            border-radius: 10px;
            background-color: ${theme.black};
          }
        }

        & .field {
          display: flex;
          align-items: center;
          margin-right: 20px;
        }

        & .section-content-row {
          display: flex;
          flex-direction: row;
          align-items: center;
          border-left: 5px solid ${theme.gray};
          padding-left: 10px;
          padding-bottom: 8px;
          margin-bottom: 8px;
        }
      }
    }
  }

  & .actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 60px;
    border-top: 0.5px solid white;
    z-index: ${({ show }) => (show ? "5" : "-1")};
  }
`

const Backtesting = () => {
  const dispatch = useDispatch()

  const [view, viewFunc] = useState(VIEW_FORM)
  const [state, stateFunc] = useState({
    start: "2015-01-01",
    end: "2024-01-01",
    coin: {
      value: "BTC",
      label: "BTC",
    },
    timeframe: {
      value: "1d",
      label: "1 day",
    },
    type: BACKTESTING_TYPES[0],
    strategy: STRATEGIES_TYPES[0],
    initial_balance: 1000,
    indicators: {},
  })

  const [loadingIndicators, loadingIndicatorsFunc] = useState(false)

  const [backtesting, backtestingFunc] = useState({
    loading: false,
    data: {},
  })

  useEffect(() => {
    loadingIndicatorsFunc(true)
    getIndicators()
      .then((response) => {
        const indicators = response.data.reduce((indicators, indicator) => {
          return {
            ...indicators,
            [indicator.name]: {
              enabled: false,
              name: indicator.name,
              parameters: Object.keys(indicator.parameters).reduce(
                (parameters, parameter) => {
                  return {
                    ...parameters,
                    [parameter]: {
                      type: indicator.parameters[parameter].type,
                      value:
                        indicator.parameters[parameter].default === "required"
                          ? ""
                          : indicator.parameters[parameter].default,
                    },
                  }
                },
                {}
              ),
            },
          }
        }, {})
        stateFunc((prevState) => ({
          ...prevState,
          indicators,
        }))
        loadingIndicatorsFunc(false)
      })
      .catch((_) => {
        loadingIndicatorsFunc(false)
      })
  }, [])

  const onChange = (key, value) => {
    stateFunc((prevState) => ({
      ...prevState,
      [key]: value,
    }))
  }

  const transformToSend = (data) => {
    const transformToSendIndicators = (data) => {
      const convert2type = (value, type) => {
        if (type === "int") {
          return parseInt(value)
        }
        if (type === "float") {
          return parseFloat(value)
        }
        return value
      }

      return Object.values(data.indicators)
        .filter((indicator) => indicator.enabled)
        .map((indicator) => ({
          ...indicator,
          parameters: Object.keys(indicator.parameters).reduce(
            (parameters, parameter) => ({
              ...parameters,
              [parameter]: convert2type(
                indicator.parameters[parameter].value,
                indicator.parameters[parameter].type
              ),
            }),
            {}
          ),
        }))
    }

    const start = new Date(`${data.start}T00:00:00Z`)
    const end = new Date(`${data.end}T00:00:00Z`)

    return {
      coins: [data.coin.value],
      initial_balance: parseInt(data.initial_balance),
      data_from: Math.floor(start.getTime() / 1000),
      data_to: Math.floor(end.getTime() / 1000),
      timeframe: data.timeframe.value,
      indicators: transformToSendIndicators(data),
      type: data.type.value.toLowerCase(),
      strategy: data.strategy.value.toLowerCase(),
    }
  }

  const onSubmit = () => {
    const transformToView = (data_) => {
      const formatRiskData = (riskData) => {
        const formattedData = {}
        for (const strategyType in riskData) {
          const strategy = riskData[strategyType]
          const formattedStrategy = {}
          for (const key in strategy) {
            formattedStrategy[key] = strategy[key].toFixed(3)
          }
          formattedData[strategyType] = formattedStrategy
        }
        return formattedData
      }

      const percentage = (start, end) => {
        return (((end - start) / start) * 100).toFixed(2)
      }

      const getProfitStrategy = (data) => {
        const start = state.initial_balance
        const end = data.final_balance
        return percentage(start, end)
      }

      const getProfitBuyAndHold = (data) => {
        const start = data.series[0].balance_buy_and_hold
        const end = data.series.at(-1).balance_buy_and_hold
        return percentage(start, end)
      }

      const getAverageReturn = (data) => {
        const sum = data.trades.reduce((acc, trade) => acc + trade.return, 0)
        const n = data.trades.length
        return (sum / n).toFixed(2)
      }

      const getBestTrade = (data) => {
        const trade = data.trades.reduce(
          (max, trade) => (trade.return > max.return ? trade : max),
          data.trades[0]
        )
        return {
          return: (trade.return * 100).toFixed(2),
          date: new Date(trade.entry_date).toLocaleDateString(),
        }
      }

      const getWorstTrade = (data) => {
        const trade = data.trades.reduce(
          (min, trade) => (trade.return < min.return ? trade : min),
          data.trades[0]
        )
        return {
          return: (trade.return * 100).toFixed(2),
          date: new Date(trade.entry_date).toLocaleDateString(),
        }
      }

      const data = data_[state.coin.value]

      return {
        ...data_,
        [state.coin.value]: {
          ...data,
          final_balance_label: data.final_balance.toFixed(2),
          profit_vs_initial_balance: getProfitStrategy(data),
          profit_vs_benchmark: percentage(
            getProfitBuyAndHold(data),
            getProfitStrategy(data)
          ),
          average_return: getAverageReturn(data),
          best_trade: getBestTrade(data),
          worst_trade: getWorstTrade(data),
          serie: data.series.map((row) => ({
            ...row,
            balance_strategy: parseFloat(row.balance_strategy.toFixed(2)),
            balance_buy_and_hold: parseFloat(
              row.balance_buy_and_hold.toFixed(2)
            ),
          })),
          risks: formatRiskData(data.risks),
        },
      }
    }

    backtestingFunc({
      loading: true,
      data: {},
    })
    runBacktesting(transformToSend(state))
      .then((response) => {
        backtestingFunc({
          loading: false,
          data: transformToView(response?.data),
        })
      })
      .catch((err) => {
        backtestingFunc((prevState) => ({
          ...prevState,
          loading: false,
        }))
        dispatch({
          type: POPUP_ACTION_OPEN,
          payload: {
            type: POPUP_TYPE_ERROR,
            message: "Could not execute backtesting",
          },
        })
      })
  }

  const onToggleView = () => {
    viewFunc((prevState) =>
      prevState === VIEW_FORM ? VIEW_BACKTESTING : VIEW_FORM
    )
  }

  const onChangeIndicatorEnabled = (key, value) => {
    const indicator = key.split(".")[0]

    stateFunc((prevState) => ({
      ...prevState,
      indicators: {
        ...prevState.indicators,
        [indicator]: {
          ...prevState.indicators[indicator],
          enabled: value,
        },
      },
    }))
  }

  const onChangeIndicatorParameter = (key, value) => {
    const indicator = key.split(".")[0]
    const parameter = key.split(".")[1]

    stateFunc((prevState) => ({
      ...prevState,
      indicators: {
        ...prevState.indicators,
        [indicator]: {
          ...prevState.indicators[indicator],
          parameters: {
            ...prevState.indicators[indicator].parameters,
            [parameter]: {
              ...prevState.indicators[indicator].parameters[parameter],
              value: value,
            },
          },
        },
      },
    }))
  }

  return (
    <View
      title="Backtesting"
      content={
        <BacktestingStyle view={view}>
          <BacktestingFormStyle show={view === VIEW_FORM}>
            <div className="sections">
              <div className="section">
                <h3>Date Range</h3>
                <div className="section-content row">
                  <div className="field">
                    <FieldDatePicker
                      label="Start"
                      name="start"
                      value={state.start}
                      onChange={onChange}
                      width={140}
                    />
                  </div>
                  <div className="field">
                    <FieldDatePicker
                      label="End"
                      name="end"
                      value={state.end}
                      onChange={onChange}
                      width={140}
                    />
                  </div>
                </div>
                <div className="section">
                  <h3>Strategy</h3>
                  <div className="section-content row">
                    <div className="field">
                      <FieldSelect
                        name={"strategy"}
                        value={state.strategy}
                        onChange={onChange}
                        width={180}
                        options={STRATEGIES_TYPES}
                      />
                    </div>
                    <div className="field">
                      <FieldSelect
                        name={"type"}
                        value={state.type}
                        onChange={onChange}
                        width={140}
                        options={BACKTESTING_TYPES}
                      />
                    </div>
                  </div>
                </div>
                <div className="section">
                  <h3>Settings</h3>
                  <div className="section-content row">
                    <div className="field">
                      <FieldInput
                        label="Initial Balance"
                        name="initial_balance"
                        value={state.initial_balance}
                        onChange={onChange}
                        width={140}
                      />
                    </div>
                    <div className="field">
                      <FieldSelect
                        label="Timeframe"
                        name="timeframe"
                        value={state.timeframe}
                        onChange={onChange}
                        width={140}
                        options={TIMEFRAMES}
                      />
                    </div>
                    <div className="field">
                      <FieldSelect
                        label="Cryptocurrency"
                        name="coin"
                        value={state.coin}
                        onChange={onChange}
                        width={165}
                        options={CRYPTOCURRENCIES}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="section">
                <h3>Indicators</h3>
                <div className="section-content">
                  <div className="indicators">
                    {loadingIndicators ? (
                      <div className="loading">
                        <BounceLoader color="white" size={32} />
                      </div>
                    ) : (
                      Object.keys(state.indicators).map((indicator) => (
                        <div className="section-content-row">
                          <div className="field">
                            <FieldSwitch
                              name={indicator}
                              label={indicator}
                              value={state.indicators[indicator].enabled}
                              onChange={onChangeIndicatorEnabled}
                            />
                          </div>
                          {state.indicators[indicator].enabled && (
                            <>
                              {Object.keys(
                                state.indicators[indicator].parameters
                              ).map((parameter) => (
                                <div className="field">
                                  <FieldInput
                                    name={`${indicator}.${parameter}`}
                                    label={parameter
                                      .split("_")
                                      .map((word) => capitalize(word))
                                      .join(" ")}
                                    value={
                                      state.indicators[indicator].parameters[
                                        parameter
                                      ].value
                                    }
                                    onChange={onChangeIndicatorParameter}
                                    width={100}
                                  />
                                </div>
                              ))}
                            </>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>
            <div className="actions">
              <Button text="Submit" onClick={onSubmit} />
            </div>
          </BacktestingFormStyle>
          <div className="divider"></div>
          <BacktestingOutputStyle>
            {backtesting.loading && (
              <div className="loading">
                <BounceLoader color="white" size="48px" />
              </div>
            )}
            {backtesting.error && "error"}
            {backtesting.data[state.coin.value] && (
              <>
                <h3>Benchmark: Buy & Hold </h3>
                <div className="boxes">
                  <Box
                    label="Final Balance"
                    value={`US$ ${
                      backtesting.data[state.coin.value]?.final_balance_label
                    }`}
                  />
                  <Box
                    label="Profit vs. Initial Balance"
                    value={`${
                      backtesting.data[state.coin.value]
                        ?.profit_vs_initial_balance
                    }%`}
                  />
                  <Box
                    label="Profit vs. Benchmark"
                    value={`${
                      backtesting.data[state.coin.value]?.profit_vs_benchmark
                    }%`}
                  />
                  <Box
                    label="# Trades"
                    value={backtesting.data[state.coin.value].trades.length}
                  />
                  <Box
                    label="Avg Return"
                    value={backtesting.data[state.coin.value]?.average_return}
                  />
                  <Box
                    label="Best Trade"
                    value={`${
                      backtesting.data[state.coin.value]?.best_trade.return
                    }% on ${
                      backtesting.data[state.coin.value]?.best_trade.date
                    }`}
                  />
                  <Box
                    label="Worst Trade"
                    value={`${
                      backtesting.data[state.coin.value]?.worst_trade.return
                    }% on ${
                      backtesting.data[state.coin.value]?.worst_trade.date
                    }`}
                  />
                </div>
                <div className="chart-container">
                  <h3>Performance Comparison</h3>
                  <StrategyComparisonChart
                    data={backtesting.data[state.coin.value]?.series}
                    colors={["#87CEEB", "#00FF00"]}
                    logScaleDefault={true}
                  />
                </div>

                <h3>Risk Analysis</h3>
                <RiskComparisonChart
                  risks={backtesting.data[state.coin.value]?.risks}
                  colors={["#87CEEB", "#00FF00"]}
                />
                <h3>Trade Details</h3>
                <TradesTableDiv>
                  <Table
                    headers={headers}
                    data={backtesting.data[state.coin.value]?.trades}
                    buildRow={buildRow}
                  />
                </TradesTableDiv>
              </>
            )}
          </BacktestingOutputStyle>
        </BacktestingStyle>
      }
    />
  )
}

export default Backtesting
