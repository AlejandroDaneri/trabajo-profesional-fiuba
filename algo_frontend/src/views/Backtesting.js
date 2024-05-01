/* Import Libs */
import React, { useEffect, useState } from "react"
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
import { getIndicators, run as runBacktesting } from "../webapi/backtesting"
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

const Indicator = ({ enabled, label, name, onChange, parameters }) => {
  return (
    <div className="section-content-row">
      <div className="field">
        <FieldSwitch
          name={name}
          label={label}
          value={enabled}
          onChange={onChange}
        />
      </div>
      {enabled &&
        <>
          {parameters.map(parameter => (
            <div className="field">
              <FieldInput
                name={parameter.name}
                label={parameter.label}
                value={parameter.value}
                onChange={onChange}
                type={parameter.type}
              />
            </div>
          ))}
        </>
      }
    </div>
  )
}

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

    rsi_buy_threshold: 30,
    rsi_sell_threshold: 70,
    rsi_rounds: 30,
    macd_enabled: true,
    macd_ema_slow: 26,
    macd_ema_fast: 12,
    macd_signal: 20,
    ema_rounds: 100,
    bbands_rounds: 9,
    bbands_factor: 2.1,
    crossing_ema_fast_rounds: 50,
    crossing_ema_slow_rounds: 200,
    crossing_sma_fast_rounds: 50,
    crossing_sma_slow_rounds: 200,
    dmi_di_rounds: 10,
    dmi_adx_rounds: 6,
    dmi_adx_threshold: 20,
    koncorde_rounds: 14,
    stochastic_buy_threshold: 80,
    stochastic_sell_threshold: 20,
    stochastic_rounds: 14
  })

  const [backtesting, backtestingFunc] = useState({
    loading: false,
    data: {}
  })

  useEffect(() => {
    getIndicators()
      .then(response => {
        console.info(response.data)
      })
      .catch(err => {
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
      let indicators = []

      if (data.rsi_enabled) {
        indicators = [...indicators, {
          name: "RSI",
          parameters: {
            buy_threshold: data.rsi_buy_threshold,
            sell_threshold: data.rsi_sell_threshold,
            rounds: data.rsi_rounds
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
            rounds: data.ema_rounds
          }
        }]
      }

      if (data.bbands_enabled) {
        indicators = [...indicators, {
          name: "BBANDS",
          parameters: {
            rounds: data.bbands_rounds,
            factor: parseFloat(data.bbands_factor)
          }
        }]
      }

      if (data.crossing_ema_enabled) {
        indicators = [...indicators, {
          name: "CrossingEMA",
          parameters: {
            fast_rounds: data.crossing_ema_fast_rounds,
            slow_rounds: data.crossing_ema_slow_rounds
          }
        }]
      }

      if (data.crossing_sma_enabled) {
        indicators = [...indicators, {
          name: "CrossingSMA",
          parameters: {
            fast_rounds: data.crossing_sma_fast_rounds,
            slow_rounds: data.crossing_sma_slow_rounds
          }
        }]
      }

      if (data.dmi_enabled) {
        indicators = [...indicators, {
          name: "DMI",
          parameters: {
            di_rounds: data.dmi_di_rounds,
            adx_rounds: data.dmi_adx_rounds,
            adx_threshold: data.dmi_adx_threshold
          }
        }]
      }

      if (data.koncorde_enabled) {
        indicators = [...indicators, {
          name: "KONCORDE",
          parameters: {
            rounds: data.koncorde_rounds,
          }
        }]
      }

      if (data.stochastic_enabled) {
        indicators = [...indicators, {
          name: "Stochastic",
          parameters: {
            rounds: data.stochastic_rounds,
            buy_threshold: data.stochastic_buy_threshold,
            sell_threshold: data.stochastic_sell_threshold,
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
                      <div className='indicators'>
                      <Indicator
                        name="rsi_enabled"
                        enabled={state.rsi_enabled}
                        label='RSI'
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.rsi_buy_threshold,
                            label: "Threshold Buy",
                            name: 'rsi_threshold_buy'
                          },
                          {
                            type: 'number',
                            value: state.rsi_sell_threshold,
                            label: "Threshold Sell",
                            name: 'rsi_threshold_sell'
                          },
                          {
                            type: 'number',
                            value: state.rsi_rounds,
                            label: "Rounds",
                            name: 'rsi_rounds'
                          },
                        ]}
                      />
                      <Indicator
                        name="macd_enabled"
                        enabled={state.macd_enabled}
                        label='MACD'
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.macd_ema_fast,
                            label: "EMA Fast",
                            name: 'macd_ema_fast'
                          },
                          {
                            type: 'number',
                            value: state.macd_ema_slow,
                            label: "EMA Slow",
                            name: 'macd_ema_slow'
                          },
                          {
                            type: 'number',
                            value: state.macd_signal,
                            label: "Signal",
                            name: 'macd_signal'
                          },
                        ]}
                      />
                      <Indicator
                        name="ema_enabled"
                        enabled={state.ema_enabled}
                        label='EMA'
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.ema_rounds,
                            label: "Rounds",
                            name: 'ema_rounds'
                          },
                        ]}
                      />
                      <Indicator
                        name="bbands_enabled"
                        label="BBANDS"
                        enabled={state.bbands_enabled}
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.bbands_rounds,
                            label: "Rounds",
                            name: 'bbands_rounds'
                          },
                          {
                            type: 'float',
                            value: state.bbands_factor,
                            label: "Factor",
                            name: 'bbands_factor'
                          }
                        ]}
                      />
                      <Indicator
                        name="crossing_ema_enabled"
                        label="Crossing EMA"
                        enabled={state.crossing_ema_enabled}
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.crossing_ema_fast_rounds,
                            label: 'Fast Rounds',
                            name: 'crossing_ema_fast_rounds',
                          },
                          {
                            type: 'number',
                            value: state.crossing_ema_slow_rounds,
                            label: 'Slow Rounds',
                            name: 'crossing_ema_slow_rounds',
                          }
                        ]}
                      />
                      <Indicator
                        name="crossing_sma_enabled"
                        label="Crossing SMA"
                        enabled={state.crossing_sma_enabled}
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.crossing_sma_fast_rounds,
                            label: 'Fast Rounds',
                            name: 'crossing_sma_fast_rounds',
                          },
                          {
                            type: 'number',
                            value: state.crossing_sma_slow_rounds,
                            label: 'Slow Rounds',
                            name: 'crossing_sma_slow_rounds',
                          }
                        ]}
                      />
                      <Indicator
                        name="dmi_enabled"
                        label="DMI"
                        enabled={state.dmi_enabled}
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.dmi_di_rounds,
                            label: 'DI Rounds',
                            name: 'dmi_di_rounds',
                          },
                          {
                            type: 'number',
                            value: state.dmi_adx_rounds,
                            label: 'ADX Rounds',
                            name: 'dmi_adx_rounds',
                          },
                          {
                            type: 'number',
                            value: state.dmi_adx_threshold,
                            label: 'ADX Threshold',
                            name: 'dmi_adx_threshold',
                          }
                        ]}
                      />
                      <Indicator
                        name="koncorde_enabled"
                        label="Koncorde"
                        enabled={state.koncorde_enabled}
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.koncorde_rounds,
                            label: 'Rounds',
                            name: 'koncorde_rounds',
                          }
                        ]}
                      />
                      <Indicator
                        name="stochastic_enabled"
                        label="Stochastic"
                        enabled={state.stochastic_enabled}
                        onChange={onChange}
                        parameters={[
                          {
                            type: 'number',
                            value: state.stochastic_rounds,
                            label: 'Rounds',
                            name: 'stochastic_rounds',
                          },
                          {
                            type: 'number',
                            value: state.stochastic_buy_threshold,
                            label: 'Buy threshold',
                            name: 'stochastic_buy_threshold',
                          },
                          {
                            type: 'number',
                            value: state.stochastic_sell_threshold,
                            label: 'Sell threshold',
                            name: 'stochastic_sell_threshold',
                          }
                        ]}
                      />
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
