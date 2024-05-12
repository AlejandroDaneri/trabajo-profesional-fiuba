/* Import Libs */
import styled from "styled-components"

/* Import Reusable Components */
import Select from "./Select"
import { theme } from "../../utils/theme"

const FieldSelectStyled = styled.div`
  & p {
    font-size: 14px;
    color: ${theme.white};
    font-weight: 600;
    padding: 0;
    margin: 0;
    margin-bottom: 8px;
  }
`

const FieldSelect = ({
  label,
  value,
  name,
  onChange,
  options,
  multiple,
  width,
}) => {
  return (
    <FieldSelectStyled>
      <p>{label}</p>
      <Select
        value={value}
        name={name}
        onChange={onChange}
        options={options}
        multiple={multiple}
        width={width}
      />
    </FieldSelectStyled>
  )
}

export default FieldSelect
