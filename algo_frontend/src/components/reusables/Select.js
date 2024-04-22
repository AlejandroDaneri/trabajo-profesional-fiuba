/* Import Libs */
import React from "react"
import ReactSelect from "react-select"
import { theme } from "../../utils/theme"

const styles = {
  control: (base, state) => {
    return {
      ...base,
      width: state.selectProps.width,
      height: state.selectProps.height,
      background: "transparent",
      border: `1px solid ${state.isFocused ? theme.btc : theme.gray}`,
      boxShadow: 'none',
      outline: 'none',
      '&:hover': {
        borderColor: theme.btc
      } 
    }
  },
  option: (styles, state) => ({
    ...styles,
    color: theme.black,
    backgroundColor: state.isSelected && theme.gray,
    '&:active': {
      backgroundColor: theme.gray
    },
    '&:hover': {
      backgroundColor: theme.gray
    } 
  }),
  singleValue: (base) => ({
    ...base,
    color: theme.white,
  }),
  multiValueRemove: (base) => ({
    ...base,
    color: theme.black,
  }),
}

const Select = ({ value, name, onChange, options, multiple, width }) => {
  const onChange_ = (value) => {
    onChange(name, value)
  }

  return (
    <ReactSelect
      value={value}
      name={name}
      onChange={onChange_}
      options={options}
      styles={styles}
      width={width}
      height={40}
      isMulti={multiple}
    />
  )
}

export default Select
