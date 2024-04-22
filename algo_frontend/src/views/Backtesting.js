/* Import Libs */
import React, { useState } from "react"
import styled from "styled-components"

import View from "../components/reusables/View"
import FieldInput from "../components/reusables/FieldInput"
import FieldSelect from "../components/reusables/FieldSelect"
import Switch from "../components/reusables/Switch"

const BacktestingStyle = styled.div`
    display: flex;
    width: 100%;

    & .form {
        display: flex;
        flex-direction: column;
        margin-left: 20px;
        margin-top: 20px;

        & .section {
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
                                <Switch id="rsiasdasda" name="rsi" value={state.rsi} onChange={onChange} />
                            </div>
                        </div>
                    </div>
                </BacktestingStyle>}
        />
    )
}

export default Backtesting