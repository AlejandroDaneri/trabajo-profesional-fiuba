/* Import Libs */
import React, { useState } from "react"
import styled from "styled-components"

/* Import Reusables Components */
import FieldSelect from "../components/reusables/FieldSelect"
import FieldSwitch from "../components/reusables/FieldSwitch"
import FieldInput from "../components/reusables/FieldInput"
import Button from "../components/Button"

/* Import WebApi */
import { add } from "../webapi/exchanges"

const ExchangeStyle = styled.div`
    display: flex;
    flex-direction: column;
`

const Exchange = ({ onCloseModal, onAdd }) => {
    const [loading, setLoading] = useState(false)

    const [state, stateFunc] = useState({
        api_key: '',
        api_secret: '',
        testing_network: true,
        alias: ''
    })

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

    return (
        <ExchangeStyle>
            <>
                <FieldSelect
                    name="provider"
                    value={state.provider}
                    onChange={onChange}
                    options={[{ value: "binance", label: "Binance" }]}
                />
                <FieldInput
                    label="API Key"
                    name="api_key"
                    value={state.api_key}
                    onChange={onChange}
                />
                <FieldInput
                    label="API Secret"
                    name="api_secret"
                    value={state.api_secret}
                    onChange={onChange}
                />
                <FieldInput
                    label="Alias"
                    name="alias"
                    value={state.alias}
                    onChange={onChange}
                />
                <FieldSwitch
                    label="Testing Network"
                    name="testing_network"
                    value={state.testing_network}
                    onChange={onChange}
                />
            </>
            <Button
                text="Submit"
                height={40}
                width={100}
                onClick={onSubmit}
                loading={loading}
            />
        </ExchangeStyle>
    )
}

export default Exchange