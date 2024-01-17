import axios from "axios"
import { getBackend } from "./trade"

export const get = () => {
  return axios.get(`${getBackend()}/api/strategy/current`)
}

export const list = () => {
  return axios.get(`${getBackend()}/api/strategy`)
}
