import axios from "axios"
import { getBackend } from "./env"

export const list = (strategyID) => {
  return axios.get(`${getBackend()}/api/trades/strategy/${strategyID}`)
}
