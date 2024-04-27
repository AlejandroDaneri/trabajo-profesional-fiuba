/* Import Libs */
import React, { useState } from "react"
import styled from "styled-components"
import "react-day-picker/dist/style.css"

/* Import Reusables Components */
import View from "../components/reusables/View"
import FieldInput from "../components/reusables/FieldInput"
import FieldSelect from "../components/reusables/FieldSelect"
import FieldSwitch from "../components/reusables/FieldSwitch"
import FieldDatePicker from "../components/reusables/FieldDatePicker"
import Button from "../components/Button"

/* Impor WebApi */
import { get as getBacktesting } from "../webapi/backtesting"

const VIEW_FORM = 0
const VIEW_BACKTESTING = 1

const BacktestingStyle = styled.div`
  display: flex;
  width: 100%;

  & .form {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
    margin-top: 20px;
    width: ${({ view }) => view === VIEW_FORM ? '800px' : '50px'};
    transition: width .5s;
    overflow: hidden;
    padding-right: 40px;
    border-right: 0.5px solid white;

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

    & .actions {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      height: 60px;
      border-top: 0.5px solid white;
    }
  }
`

const Backtesting = () => {
  const [view, viewFunc] = useState(VIEW_FORM)
  const [state, stateFunc] = useState({})
  const [backtesting, backtestingFunc] = useState({})

  const onChange = (key, value) => {
    stateFunc((prevState) => ({
      ...prevState,
      [key]: value,
    }))
  }

  const transformToSend = (data) => {
    const start = new Date(`${data.start}T00:00:00Z`)
    const end = new Date(`${data.end}T00:00:00Z`)

    return {
      symbol: data.coin.value,
      initial_balance: data.initial_balance,
      start: Math.floor(start.getTime() / 1000),
      end: Math.floor(end.getTime() / 1000),
    };
  }

  const onSubmit = () => {
    viewFunc(VIEW_BACKTESTING)
    getBacktesting(transformToSend(state))
      .then((response) => {
        backtestingFunc(response?.data)
      })
      .catch((_) => {})
  }

  const onBack = () => {
    viewFunc(VIEW_FORM)
  }

  return (
    <View
      title="Backtesting"
      content={
        <BacktestingStyle view={view}>
          <div className="form">
          {view === VIEW_FORM && <>
              <>
                <div className="section">
                  <h3>Date Range</h3>
                  <div className="section-content row">
                    <div className="field">
                      <FieldDatePicker
                        label="Start"
                        name="start"
                        onChange={onChange}
                        width={140}
                      />
                    </div>
                    <div className="field">
                      <FieldDatePicker
                        label="End"
                        name="end"
                        onChange={onChange}
                        width={140}
                      />
                    </div>
                  </div>
                </div>
                <div className="section">
                  <h3>Date Range</h3>
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
                    <FieldSwitch
                      name="rsi"
                      label="RSI"
                      value={state.rsi}
                      onChange={onChange}
                    />
                    <FieldSwitch
                      name="macd"
                      label="MACD"
                      value={state.macd}
                      onChange={onChange}
                    />
                    <FieldSwitch
                      name="ema"
                      label="EMA"
                      value={state.ema}
                      onChange={onChange}
                    />
                  </div>
                </div>
              </>
              <div className="actions">
                <Button text="Submit" onClick={onSubmit} />
              </div>
            </>}
          </div>
          {view === VIEW_BACKTESTING && (
            <div>
              Final Balance: {backtesting.final_balance}
              <Button text="Back" onClick={onBack} />
            </div>
          )}
        </BacktestingStyle>
      }
    />
  );
};

export default Backtesting;
