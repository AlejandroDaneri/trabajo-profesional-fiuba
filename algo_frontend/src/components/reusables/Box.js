/* Import Libs */
import React from "react"
import styled from "styled-components"

const BoxStyled = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 50px;
    border: 0.1px solid #e5e7eb;
    border-radius: 4px;
    padding: 10px;
    background: linear-gradient(132.03deg, rgba(21,24,37,.4) 0%, rgba(11,10,7,.4) 100%);

    & .label {
        color: #a5a8b6;
    }

    & .value {
        display: flex;
        font-size: 14px;
        font-weight: 600;
        min-width: 120px;
    }
`

const Box = ({ label, value }) => {
    return (
        <BoxStyled>
            <div className="label">{label}</div>
            <div className="value">{value}</div>
        </BoxStyled>
    )
}

export default Box