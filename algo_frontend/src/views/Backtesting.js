/* Import Libs */
import React, { useState } from "react"
import styled from "styled-components"
import "react-day-picker/dist/style.css"

/* Import Reusables Components */
import View from "../components/reusables/View"
import FieldInput from "../components/reusables/FieldInput"
import FieldSelect from "../components/reusables/FieldSelect"
import FieldSwitch from "../components/reusables/FieldSwitch"
import Button from "../components/Button"


/* Impor WebApi */
import { get as getBacktesting } from "../webapi/backtesting"
import Datepicker from "../components/reusables/DatePicker"
import DatePicker from "../components/reusables/DatePicker"

const BacktestingStyle = styled.div`
  display: flex;
  width: 100%;

  & .form {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
    margin-top: 20px;

    width: 400px;
    border-right: 0.5px solid white;
    padding-right: 40px;

    & .section {
      margin-bottom: 20px;
      & h3 {
        border-bottom: 0.5px solid white;
        padding-bottom: 5px;
        margin: 0;
      }

      & .section-content {
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
`;

const Backtesting = () => {
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
  };

  const onSubmit = () => {
    getBacktesting(transformToSend(state))
      .then((response) => {
        backtestingFunc(response?.data);
      })
      .catch((_) => {});
  }

  return (
    <View
      title="Backtesting"
      content={
        <BacktestingStyle>
          <div className="form">
            <div className="section">
              <h3>Basic</h3>
              <div className="section-content">
                <DatePicker name="start" onChange={onChange} />
                <FieldInput
                  label="Initial Balance"
                  name="initial_balance"
                  value={state.initial_balance}
                  onChange={onChange}
                  width={140}
                />
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
            <div className="actions">
              <Button text="Submit" onClick={onSubmit} />
            </div>
          </div>
          <div>Final Balance: {backtesting.final_balance}</div>
        </BacktestingStyle>
      }
    />
  );
};

export default Backtesting;
