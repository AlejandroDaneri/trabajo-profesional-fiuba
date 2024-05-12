/* Import Libs */
import React, { useEffect, useRef, useState } from "react"
import { format, isValid, parse } from "date-fns"
import { DayPicker as DayPickerLib } from "react-day-picker"

/* Import Reusables Compontens */
import Input from "./Input"
import styled from "styled-components"
import { theme } from "../../utils/theme"

const FieldDatePickerStyle = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;

  & p {
    width: 100%;
    text-align: left;
    font-size: 14px;
    color: ${theme.white};
    font-weight: 600;
    padding: 0;
    margin: 0;
    margin-bottom: 8px;
  }

  & .my-day-picker {
    background-color: ${theme.black};
    padding: 10px;
    --rdp-accent-color: ${theme.btc};
    --rdp-background-color: ${theme.btc};
    box-shadow: 0 1px 10px rgba(0, 0, 0, 0.2), 0 4px 5px rgba(0, 0, 0, 0.3),
      0 2px 4px -1px rgba(0, 0, 0, 0.4);
  }

  & .day-picker-container-1 {
    position: relative;
    right: 125px;
    z-index: 1;

    & .day-picker-container-2 {
      position: absolute;
    }
  }

  & .row {
    display: flex;
    align-items: center;

    & i {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-left: 10px;
      border: 1px solid white;
      width: 35px;
      height: 35px;
      font-size: 18px;
      border-radius: 30px;
      cursor: pointer;
    }
  }
`

const FieldDatePicker = ({ onChange, name, value, label, width }) => {
  const ref = useRef()

  const [selected, setSelected] = useState()
  const [selectorOpened, selectorOpenedFunc] = useState(false)

  const handleInputChange = (e) => {
    onChange(name, e.currentTarget.value)
    const date = parse(e.currentTarget.value, "y-MM-dd", new Date())
    if (isValid(date)) {
      setSelected(date)
    } else {
      setSelected(undefined)
    }
  }

  const handleDaySelect = (date) => {
    setSelected(date)
    if (date) {
      onChange(name, format(date, "y-MM-dd"))
    } else {
      onChange(name, "")
    }
  }

  const onToggle = () => {
    selectorOpenedFunc((prevState) => !prevState)
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        selectorOpenedFunc(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  return (
    <FieldDatePickerStyle>
      <p>{label}</p>
      <div className="row">
        <Input value={value} onChange={handleInputChange} width={width} />
        <i className="material-icons" onClick={onToggle}>
          event
        </i>
      </div>
      {selectorOpened && (
        <div className="day-picker-container-1" ref={ref}>
          <div className="day-picker-container-2">
            <DayPickerLib
              initialFocus={true}
              mode="single"
              defaultMonth={selected}
              selected={selected}
              onSelect={handleDaySelect}
              className="my-day-picker"
            />
          </div>
        </div>
      )}
    </FieldDatePickerStyle>
  )
}

export default FieldDatePicker
