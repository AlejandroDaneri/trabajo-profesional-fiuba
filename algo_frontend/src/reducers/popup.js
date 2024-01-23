import { POPUP_ACTION_CLOSE, POPUP_ACTION_OPEN } from "../components/Popup"

const INITIAL_STATE = {}

export const popup = (state = INITIAL_STATE, action) => {
  const { type, payload } = action
  switch (type) {
    case POPUP_ACTION_OPEN: {
      return {
        open: true,
        message: payload,
      }
    }
    case POPUP_ACTION_CLOSE: {
      return {
        open: false,
        message: payload,
      }
    }
    default: {
      return state
    }
  }
}

export default popup
