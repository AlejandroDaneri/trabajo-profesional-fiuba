/* Import Libs */
import React from "react"
import { Snackbar, SnackbarContent } from "@material-ui/core"
import { useSelector, useDispatch } from "react-redux"
import { theme } from "../utils/theme"

const POPUP_POSITION_Y = "bottom"
const POPUP_POSITION_X = "right"
const POPUP_TEXT_SIZE = "14px"
const POPUP_DURATION = 2000

export const POPUP_ACTION_OPEN = "POPUP_ACTION_OPEN"
export const POPUP_ACTION_CLOSE = "POPUP_ACTION_CLOSE"
export const POPUP_TYPE_SUCCESS = "POPUP_TYPE_SUCCESS"
export const POPUP_TYPE_ERROR = "POPUP_TYPE_ERROR"

const Popup = () => {
  const popup = useSelector((state) => state.popup)
  const { open, message } = popup
  const dispatch = useDispatch()

  const handleClose = () => {
    dispatch({
      type: POPUP_ACTION_CLOSE,
      payload: {
        type: popup.message?.type,
        message: popup.message?.message,
      },
    })
  }

  return (
    <Snackbar
      open={open}
      onClose={handleClose}
      anchorOrigin={{
        vertical: POPUP_POSITION_Y,
        horizontal: POPUP_POSITION_X,
      }}
      autoHideDuration={message?.autoHideDisabled ? undefined : POPUP_DURATION}
    >
      <SnackbarContent
        message={message?.message}
        style={{
          color: theme.white,
          backgroundColor:
            message?.type === POPUP_TYPE_SUCCESS ? theme.green : theme.red,
          fontSize: POPUP_TEXT_SIZE,
          fontWeight: 600,
        }}
      />
    </Snackbar>
  )
}

export default Popup
