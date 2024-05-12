/* Import Libs */
import React from "react"
import styled from "styled-components"
import Switch from "./Switch"
import { theme } from "../../utils/theme"

const FieldSwitchStyle = styled.div`
  & p {
    font-size: 14px;
    color: ${theme.white};
    padding: 0;
    margin: 0;
    margin-bottom: 8px;
    font-weight: 600;
  }
`

const FieldSwitch = ({ label, value, onChange, name, id }) => {
  return (
    <FieldSwitchStyle>
      <p>{label}</p>
      <Switch id={name} name={name} value={value} onChange={onChange} />
    </FieldSwitchStyle>
  )
}

export default FieldSwitch
