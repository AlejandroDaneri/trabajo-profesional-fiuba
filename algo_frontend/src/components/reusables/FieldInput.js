/* Import Libs */
import React from "react"
import styled from "styled-components"

/* Import Reusables Components */
import Input from "./Input"
import { theme } from "../../utils/theme"

const FieldInputStyle = styled.div`
    display: flex;
    flex-direction: column;

    & p {
        font-size: 14px;
        color: ${theme.white};
        font-weight: 600;
        padding: 0;
        margin: 0;
        margin-bottom: 8px;
    }
`

const FieldInput = ({label, name, value, onChange, width, type}) => {

    const onChange_ = (e) => {
        onChange(e.target.name, e.target.value)
    }

    return (
        <FieldInputStyle>
            <p>{label}</p>
            <Input value={value} name={name} onChange={onChange_} width={width} type={type} />
        </FieldInputStyle>
    )
}

export default FieldInput