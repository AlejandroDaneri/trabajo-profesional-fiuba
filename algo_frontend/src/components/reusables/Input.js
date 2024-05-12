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
    padding: 0;
    padding-left: 8px;
    margin: 0;
    font-size: 14px;
    width: ${({width}) => `${width - 10}px`};
    max-width: ${({width}) => `${width - 10}px`};
    height: 38px;
    max-height: 38px;

    &:hover {
        border: 1px solid ${theme.btc}
    }
`

const Input = ({width, onChange, value, name, type}) => {
    return <InputStyle name={name} value={value} width={width} onChange={onChange} type={type} /> 
}

export default Input