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

const FieldInput = ({label, value, onChange}) => {
    return (
        <FieldInputStyle>
            <p>{label}</p>
            <Input value={value} onChange={onChange} />
        </FieldInputStyle>
    )
}

export default FieldInput