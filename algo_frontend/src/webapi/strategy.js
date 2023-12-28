import axios from "axios"
import { getBackend } from "./trade"

export const getStrategy = () => {
  return axios.get(`${getBackend()}/api/strategy`)
}
