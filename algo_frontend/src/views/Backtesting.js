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
    indicators: {}
  })

  const [backtesting, backtestingFunc] = useState({
    loading: false,
    data: {}
  })

  useEffect(() => {
    getIndicators()
      .then(response => {
        console.info(response.data)
        const indicators = response.data.reduce((indicators, indicator) => {
          return {
            ...indicators,
            [indicator.name]: {
              ...indicator,
              enabled: false
            }
          }
        }, {})
        stateFunc(prevState => ({
          ...prevState,
          indicators
        }))
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

  const onChangeIndicator = (key, value) => {
    const indicator = key.split('.')[0]
    const field = key.split('.')[1]

    stateFunc(prevState => ({
      ...prevState,
      indicators: {
        ...prevState.indicators,
        [indicator]: {
          ...prevState.indicators[indicator],
          [field]: value
        }
      }
    }))
  }

  console.info(state.indicators)

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
                        {Object.keys(state.indicators).map(indicator => (
                          <div className="section-content-row">
                            <div className="field">
                              <FieldSwitch
                                name={`${indicator}.enabled`}
                                label={indicator}
                                value={state.indicators[indicator].enabled}
                                onChange={onChangeIndicator}
                              />
                            </div>
                            {state.indicators[indicator].enabled &&
                              <>
                                {Object.keys(state.indicators[indicator].parameters).map(parameter => (
                                  <div className="field">
                                    <FieldInput
                                      name={parameter}
                                      label={parameter}
                                      value={state.indicators[indicator].parameters[parameter].value}
                                      type={state.indicators[indicator].parameters[parameter].type}
                                      onChange={onChange}
                                    />
                                  </div>
                                ))}
                              </>
                            }
                          </div>
                        ))}
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
