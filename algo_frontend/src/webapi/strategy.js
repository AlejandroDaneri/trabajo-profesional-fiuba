import axios from "axios"
import { getBackend } from "./env"

export const getRunning = () => {
  return axios.get(`${getBackend()}/api/strategy/running`)
}

export const list = () => {
  return axios.get(`${getBackend()}/api/strategy`)
}

export const start = (id) => {
  return axios.put(`${getBackend()}/api/strategy/${id}/start`)
}

export const stop = (id) => {
  return axios.put(`${getBackend()}/api/strategy/${id}/stop`)
}

export const remove = (id) => {
  return axios.delete(`${getBackend()}/api/strategy/${id}`)
}

export const add = (strategy) => {
  return axios.post(`${getBackend()}/api/strategy`, strategy)
}
