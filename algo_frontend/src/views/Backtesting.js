/* Import Libs */
import React, { useState } from "react"
import styled from "styled-components"

/* Import Reusables Components */
import View from "../components/reusables/View"
import FieldInput from "../components/reusables/FieldInput"
import FieldSelect from "../components/reusables/FieldSelect"
import FieldSwitch from "../components/reusables/FieldSwitch"
import Button from "../components/Button"

/* Impor WebApi */
import { get as getBacktesting } from "../webapi/backtesting"

const BacktestingStyle = styled.div`
    display: flex;
    width: 100%;

    & .form {
        display: flex;
        flex-direction: column;
        margin-left: 20px;
        margin-top: 20px;

        & .section {
            margin-bottom: 20px;
            & h3 {
                border-bottom: 1px solid white;
                padding-bottom: 5px;
                margin: 0;
            }

            & .section-content {
            }
        }
    }
`

const Backtesting = () => {

    const [state, stateFunc] = useState({})

    const onChange = (key, value) => {
        stateFunc(prevState => ({
            ...prevState,
            [key]: value
        }))
    }

    const transformToSend = (data) => {
        return {
            ...data,
            coin: data.coin.value
        }
    }

    const onSubmit = () => {
        getBacktesting(transformToSend(state))
            .then(_ => {})
            .catch(_ => {})
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
                                            label: "BTC"
                                        },
                                        {
                                            value: "ETH",
                                            label: "ETH"
                                        }
                                    ]}
                                />
                            </div>
                        </div>
                        <div className="section">
                            <h3>Indicators</h3>
                            <div className="section-content">
                                <FieldSwitch name="rsi" label="RSI" value={state.rsi} onChange={onChange} />
                                <FieldSwitch name="macd" label="MACD" value={state.macd} onChange={onChange} />
                                <FieldSwitch name="ema" label="EMA" value={state.ema} onChange={onChange} />
                            </div>
                        </div>
                        
                        <Button text="Submit" onClick={onSubmit} />
                    </div>
                </BacktestingStyle>}
        />
    )
}

export default Backtesting