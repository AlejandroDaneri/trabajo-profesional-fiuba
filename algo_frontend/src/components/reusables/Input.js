/* Import Libs */
import React from "react"
import styled from "styled-components"
import { theme } from "../../utils/theme"

const InputStyle = styled.input`
    background: transparent;
    border: 1px solid ${theme.gray};
    border-radius: 4px;
    color: ${theme.white};
    outline: none;
    max-height: 40px;
    margin: 0;

    &:hover {
        border: 1px solid ${theme.btc}
    }
`

const Input = () => {
    return <InputStyle /> 
}

export default Input