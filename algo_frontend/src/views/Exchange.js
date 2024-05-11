/* Import Libs */
import React, { useEffect, useState } from "react"
import styled from "styled-components"

/* Import Reusables Components */
import FieldSelect from "../components/reusables/FieldSelect"
import FieldSwitch from "../components/reusables/FieldSwitch"
import FieldInput from "../components/reusables/FieldInput"
import Button from "../components/Button"

/* Import WebApi */
import { add, get } from "../webapi/exchanges"

const ExchangeStyle = styled.div`
    display: flex;
    flex-direction: column;
    padding: 20px;

    & .field {
        margin-right: 20px;
    }

    & .row {
        display: flex;
        flex-direction: row;
        margin-bottom: 20px;
    }

    & .column {
        display: flex;
        flex-direction: column;
    }

    & .actions {
        display: flex;
        justify-content: right;

        & .first {
            margin-right: 10px;
        }
    }
`

const Exchange = ({ id, open, onCloseModal, onAdd }) => {
    const [loading, setLoading] = useState(false)

    const [state, stateFunc] = useState({
        api_key: '',
        api_secret: '',
        testing_network: true,
        alias: ''
    })

    useEffect(() => {
        if (open) {
            if (id) {
                get(id)
                    .then(response => {
                        stateFunc(response?.data)
                    })
            } else {
                stateFunc({
                    api_key: '',
                    api_secret: '',
                    testing_network: true,
                    alias: ''
                })
            }
        }
    }, [open]) // eslint-disable-line

    const transformToSend = (data) => {
        return {
          api_key: data.api_key,
          api_secret: data.api_secret,
          alias: data.alias,
          testing_network: data.testing_network
        }
    }

    const onSubmit = () => {
        setLoading(true)
        add(transformToSend(state))
            .then(() => {
                setLoading(false)
                onCloseModal()
                onAdd()
            })
            .catch(() => {
                setLoading(false)
            })
    }

    const onChange = (key, value) => {
        stateFunc(prevState => ({
          ...prevState,
          [key]: value
        }))
    }

    const onCancel = () => {
        onCloseModal()
    }

    return (
        <ExchangeStyle>
            <>
                <div className="row">
                    <div className="field">
                        <FieldInput
                            label="Alias"
                            name="alias"
                            value={state.alias}
                            onChange={onChange}
                            width='300'
                        />
                    </div>
                    <FieldSelect
                        label="Provider"
                        name="provider"
                        value={state.provider}
                        onChange={onChange}
                        options={[{ value: "binance", label: "Binance" }]}
                        width='300'
                    />
                </div>

                {state.provider?.value === "binance" && <div className="column">
                    <div className="row">
                        <FieldInput
                            label="API Key"
                            name="api_key"
                            value={state.api_key}
                            onChange={onChange}
                            width='620'
                        />
                    </div>
                    <div className="row">
                        <FieldInput
                            label="API Secret"
                            name="api_secret"
                            value={state.api_secret}
                            onChange={onChange}
                            width='620'
                        />
                    </div>
                    <div className="row">
                        <FieldSwitch
                            label="Testing Network"
                            name="testing_network"
                            value={state.testing_network}
                            onChange={onChange}
                        />
                    </div>
                </div>}
            </>
            <div className="actions">
                <div className="first">
                    <Button
                        text="Cancel"
                        height={30}
                        width={100}
                        onClick={onCancel}
                    />
                </div>
                <Button
                    text="Submit"
                    height={30}
                    width={100}
                    onClick={onSubmit}
                    loading={loading}
                />
            </div>
        </ExchangeStyle>
    )
}

export default Exchange