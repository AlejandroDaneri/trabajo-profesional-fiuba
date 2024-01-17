import axios from "axios"
import { getBackend } from "./trade"

export const get = () => {
  return axios.get(`${getBackend()}/api/strategy/running`)
}

export const list = () => {
  return axios.get(`${getBackend()}/api/strategy`)
}

export const stop = (id) => {
  return axios.put(`${getBackend()}/api/strategy/stop/${id}`)
}
