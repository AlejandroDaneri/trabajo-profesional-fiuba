/* Import Libs */
import React, { useState } from "react"
import styled from "styled-components"
import BounceLoader from "react-spinners/BounceLoader"
import "react-day-picker/dist/style.css"

/* Import Reusables Components */
import View from "../components/reusables/View"
import FieldInput from "../components/reusables/FieldInput"
import FieldSelect from "../components/reusables/FieldSelect"
import FieldSwitch from "../components/reusables/FieldSwitch"
import FieldDatePicker from "../components/reusables/FieldDatePicker"
import Button from "../components/Button"

/* Impor WebApi */
import { run as runBacktesting } from "../webapi/backtesting"
import { theme } from "../utils/theme"

const VIEW_FORM = 0
const VIEW_BACKTESTING = 1

const BacktestingStyle = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
  height: calc(100vh - 40px - 84px);
  overflow: hidden;

  & .form {
    display: flex;
    flex-direction: column;
    padding-left: 20px;
    padding-top: 20px;
    width: ${({ view }) => view === VIEW_FORM ? '600px' : '10px'};
    transition: width .5s;
    padding-right: 20px;
    background: ${theme.dark};

    & .sections {
      display: flex;
      flex-direction: column;

      & .section {
        margin-bottom: 20px;
  
        & h3 {
          border-bottom: 0.5px solid white;
          padding-bottom: 5px;
          margin: 0;
        }
  
        & .section-content.row {
          flex-direction: row;
        }
  
        & .section-content {
          display: flex;
          flex-direction: column;
  
          & .field {
            margin-right: 20px;
          }
  
          & .row {
            display: flex;
            flex-direction: row;
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
    }
  }

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
    align-items: center;

    & .box {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 50px;
      border: 1px solid white;
      padding: 10px;
      border-radius: 4px;

      & .label {
        color: #a5a8b6;
      }

      & .value {
        display: flex;
        font-weight: 800;

        & .currency-wrapper {
          margin-right: 5px;
        }
      }
    }
  }
`

const Backtesting = () => {
  const [view, viewFunc] = useState(VIEW_FORM)
  const [state, stateFunc] = useState({
    start: '2015-01-01',
    end: '2024-01-01',
    coin: {
      value: 'BTC',
      label: 'BTC'
    },
    timeframe: {
      value: '1D',
      label: '1 day'
    },
    initial_balance: 1000,

    macd_enabled: true,
    macd_ema_slow: 26,
    macd_ema_fast: 12,
    macd_signal: 20
  })

  const [backtesting, backtestingFunc] = useState({
    loading: false,
    data: {}
  })

  const onChange = (key, value) => {
    stateFunc((prevState) => ({
      ...prevState,
      [key]: value,
    }))
  }

  const transformToSend = (data) => {

    const transformToSendIndicators = (data) => {
      let indicators = []

      if (data.rsi_enabled) {
        indicators = [...indicators, {
          name: "RSI",
          parameters: {
            buy_threshold: parseInt(data.rsi_buy_threshold),
            sell_threshold: parseInt(data.rsi_sell_threshold),
            rounds: parseInt(data.rsi_rounds)
          }
        }]
      }

      if (data.macd_enabled) {
        indicators = [...indicators, {
          name: "MACD",
          parameters: {
            slow: data.macd_ema_slow,
            fast: data.macd_ema_fast,
            smoothed: data.macd_signal
          }
        }]
      }

      if (data.ema_enabled) {
        indicators = [...indicators, {
          name: "EMA",
          parameters: {
            rounds: parseInt(data.ema_rounds)
          }
        }]
      }

      return indicators
    }

    const start = new Date(`${data.start}T00:00:00Z`)
    const end = new Date(`${data.end}T00:00:00Z`)

    return {
      coins: [data.coin.value],
      initial_balance: parseInt(data.initial_balance),
      data_from: Math.floor(start.getTime() / 1000),
      data_to: Math.floor(end.getTime() / 1000),
      timeframe: data.timeframe.value.toUpperCase(),
      indicators: transformToSendIndicators(data) 
    }
  }

  const onSubmit = () => {
    backtestingFunc({
      loading: true,
      data: {}
    })
    viewFunc(VIEW_BACKTESTING)
    runBacktesting(transformToSend(state))
      .then((response) => {
        backtestingFunc({
          loading: false,
          data: response?.data
        })
      })
      .catch((_) => {})
  }

  const onToggleView = () => {
    viewFunc(prevState => prevState === VIEW_FORM ? VIEW_BACKTESTING : VIEW_FORM)
  }

  return (
    <View
      title="Backtesting"
      content={
        <BacktestingStyle view={view}>
          <div className="form">
            {view === VIEW_FORM && <>
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
                </div>
                <div className="section">
                    <h3>Basic</h3>
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
                          options={[
                            {
                              value: '1M',
                              label: '1 min'
                            },
                            {
                              value: '5M',
                              label: '5 min'
                            },
                            {
                              value: '1H',
                              label: '1 hour'
                            },
                            {
                              value: '1D',
                              label: '1 day'
                            }
                          ]}
                        />
                      </div>
                      <div className="field">
                        <FieldSelect
                          label="Cryptocurrency"
                          name="coin"
                          value={state.coin}
                          onChange={onChange}
                          width={165}
                          options={[
                            {
                              value: "BTC",
                              label: "BTC",
                            },
                            {
                              value: "ETH",
                              label: "ETH",
                            },
                          ]}
                        />
                      </div>
                    </div>
                </div>
                <div className="section">
                    <h3>Indicators</h3>
                    <div className="section-content">
                      <div className="row">
                        <div className="field">
                          <FieldSwitch
                            name="rsi_enabled"
                            label="RSI"
                            value={state.rsi_enabled}
                            onChange={onChange}
                          />
                        </div>
                        {state.rsi_enabled &&
                          <>
                            <div className="field">
                              <FieldInput
                                name="rsi_threshold_buy"
                                label="Threshold Buy"
                                value={state.rsi_threshold_buy}
                                onChange={onChange}
                              />
                            </div>
                            <div className="field">
                              <FieldInput
                                name="rsi_threshold_sell"
                                label="Threshold Sell"
                                value={state.rsi_threshold_sell}
                                onChange={onChange}
                              />
                            </div>
                            <div className="field">
                              <FieldInput
                                name="rsi_rounds"
                                label="Rounds"
                                value={state.rsi_rounds}
                                onChange={onChange}
                              />
                            </div>
                          </>
                        }
                      </div>
                      <div className="row">
                        <div className="field">
                          <FieldSwitch
                            name="macd_enabled"
                            label="MACD"
                            value={state.macd_enabled}
                            onChange={onChange}
                          />
                        </div>
                        {state.macd_enabled && <>
                          <div className="field">
                            <FieldInput
                              name="macd_ema_fast"
                              label="EMA Fast"
                              value={state.macd_ema_fast}
                              onChange={onChange}
                              type='number'
                            />
                          </div>
                          <div className="field">
                            <FieldInput
                              name="macd_ema_slow"
                              label="EMA Slow"
                              value={state.macd_ema_slow}
                              onChange={onChange}
                              type='number'
                            />
                          </div>
                          <div className="field">
                            <FieldInput
                              name="macd_signal"
                              label="Signal"
                              value={state.macd_signal}
                              onChange={onChange}
                              type='number'
                            />
                          </div>
                        </>}
                      </div>
                      <div className="row">
                        <div className="field">
                          <FieldSwitch
                            name="ema_enabled"
                            label="EMA"
                            value={state.ema_enabled}
                            onChange={onChange}
                          />
                        </div>
                        {state.ema_enabled && <>
                          <div className="field">
                            <FieldInput
                              name="ema_rounds"
                              label="Rounds"
                              value={state.ema_rounds}
                              onChange={onChange}
                              initial={100}
                            />
                          </div>
                        </>}
                      </div>
                    </div>
                </div>
              </div>
              <div className="actions">
                <Button text="Submit" onClick={onSubmit} />
              </div>
            </>}
          </div>
          <div className="divider"></div>
          <div className="button-back">
            <Button
              width={30}
              height={30}
              text={<i className="material-icons">{view === VIEW_FORM ? 'arrow_back' : 'arrow_forward'}</i>}
              onClick={onToggleView}
              background={theme.btc}
              circle
            />
          </div>
          {view === VIEW_BACKTESTING && (
            <div className="backtesting">
              {backtesting.loading && <BounceLoader color='white' size='48px' />}
              {backtesting.error && 'error'}
              {backtesting.data[state.coin.value] && (
                <div className="box">
                  <div className="label">Final Balance</div>
                  <div className="value">{backtesting.data[state.coin.value].final_balance.toFixed(2)}$</div>
                </div>
              )}
            </div>
          )}
        </BacktestingStyle>
      }
    />
  )
}

export default Backtesting;
