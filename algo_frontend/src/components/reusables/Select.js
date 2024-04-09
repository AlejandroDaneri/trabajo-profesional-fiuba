/* Import Libs */
import React from "react"
import ReactSelect from "react-select"

const styles = {
  control: (base, state) => {
    return {
      ...base,
      width: state.selectProps.width,
      height: state.selectProps.height,
      background: "transparent",
    }
  },
  option: (styles) => ({
    ...styles,
    color: "black",
  }),
  multiValueRemove: (base) => ({
    ...base,
    color: "black",
  }),
}

const Select = ({ value, name, onChange, options }) => {
  const onChange_ = (value) => {
    onChange(name, value)
  }

  return (
    <ReactSelect
      isMulti
      value={value}
      name={name}
      onChange={onChange_}
      options={options}
      styles={styles}
      width={800}
      height={60}
    />
  )
}

export default Select
