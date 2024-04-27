/* Import Libs */
import React from 'react'
import styled, { css } from 'styled-components'
import { theme } from '../../utils/theme'

const SwitchStyle = styled.div`
    cursor: pointer;

    & .switch-input {
        position: relative;
        width: 45px;
        height: 25px;
        border-radius: 30px;
        background-color: transparent;
        border: ${({ value }) => value ? `1px solid ${theme.white}` : '1px solid #E6E6E6'};
        transition: all 0.1s ease-out;
        

        & input[type='checkbox'] {
            visibility: hidden;
            position: absolute;
            width: 45px;
            height: 25px;
            top: -1px;
            left: -1px;
        }

        & .rail {
            position: absolute;
            width: 45px;
            height: 25px;
            top: -1px;
            left: -1px;
            border-radius: 30px;
        }

        & .thumb {
            cursor: pointer;
            position: absolute;
            ${({ value }) => {
                if (value) {
                return css`
                    right: -1px;
                `
                } else {
                return css`
                    left: -1px;
                `
                }
            }}
            top: -1px;
            width: 25px;
            height: 25px;
            border-radius: 12px;
            background-color: ${({value}) => value ? theme.btc : theme.gray};
            border: 1px solid ${theme.white};
        }
    } 
`

const Switch = ({
  id,
  name,
  onChange,
  value,
}) => {
    const onChange_ = (e) => {
        onChange(e.target.name, e.target.checked)
    }

    return (
        <SwitchStyle value={value}>
            <div className='switch-input'>
            <input
                type='checkbox'
                id={id}
                name={name}
                checked={value}
                onChange={onChange_}
            />

            <label className='rail' htmlFor={id} />

            <label className='thumb' htmlFor={id} />
            </div>
        </SwitchStyle>
    )
}

export default Switch
