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
        margin-bottom: 8px;
        font-weight: 600;
    }
`

const FieldInput = ({label, name, value, onChange, width}) => {
    const onChange_ = (e) => {
        onChange(e.target.name, e.target.value)
    }
    return (
        <FieldInputStyle>
            <p>{label}</p>
            <Input value={value} name={name} onChange={onChange_} width={width} />
        </FieldInputStyle>
    )
}

export default FieldInput