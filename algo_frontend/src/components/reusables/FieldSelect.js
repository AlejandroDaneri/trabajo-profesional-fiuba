/* Import Libs */
import styled from "styled-components"

/* Import Reusable Components */
import Select from "./Select"

const FieldSelectStyled = styled.div``

const FieldSelect = ({ label, value, name, onChange, options }) => {
  return (
    <FieldSelectStyled>
      <p>{label}</p>
      <Select value={value} name={name} onChange={onChange} options={options} />
    </FieldSelectStyled>
  )
}

export default FieldSelect
