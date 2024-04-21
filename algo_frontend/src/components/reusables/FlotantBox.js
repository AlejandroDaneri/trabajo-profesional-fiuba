/* Import Libs */
import React, { useRef, useState, useContext, createContext } from "react"
import styled from "styled-components"
import { v4 } from "uuid"
import { theme } from "../../utils/theme"

const FlotantBoxStyle = styled.div`
  display: flex;
  justify-content: center;

  & .beside {
    min-width: ${({ besideWidth }) => besideWidth + "px"};
  }

  & .container-1 {
    display: flex;
    justify-content: center;
    position: relative;

    & .container-2 {
      position: absolute;
      top: 0px;
      right: ${({ buttonWidth }) => buttonWidth + 5 + "px"};
      z-index: 1;
      border: 2px solid ${theme.white};
      background: ${theme.grayDark};
      color: ${theme.white};
      height: auto;
      padding: 5px;
    }
  }
`

const IDContext = createContext()

export function FlotantBoxProvider({ children }) {
  const [sharedID, sharedIDFunc] = useState("")

  const setSharedID = (newState) => {
    sharedIDFunc((prevState) => {
      if (prevState === newState) {
        return ""
      } else {
        return newState
      }
    })
  }

  return (
    <IDContext.Provider value={{ sharedID, setSharedID }}>
      {children}
    </IDContext.Provider>
  )
}

export function useID() {
  return useContext(IDContext)
}

const FlotantBox = ({ button, content, beside }) => {
  const buttonRef = useRef()
  const besideRef = useRef()

  const [id] = useState(v4())
  const { sharedID, setSharedID } = useID()

  const open = sharedID === id

  const onClick = () => {
    setSharedID(id)
  }

  return (
    <FlotantBoxStyle
      besideWidth={besideRef?.current?.clientWidth}
      buttonWidth={buttonRef?.current?.clientWidth}
    >
      <div className="container-1">
        {beside && (
          <div className="beside">
            {!open && React.cloneElement(beside, { ref: besideRef })}
          </div>
        )}
        {React.cloneElement(button, { onClick: onClick, ref: buttonRef })}
        {open && <div className="container-2">{content}</div>}
      </div>
    </FlotantBoxStyle>
  )
}

export default FlotantBox
