import axios from "axios";
import { getBackend } from "./env"

export const add = (exchange) => {
  return axios.post(`${getBackend()}/api/exchanges`, exchange)
}

export const remove = (id) => {
  return axios.delete(`${getBackend()}/api/exchanges/${id}`)
}

export const get = (id) => {
  return axios.get(`${getBackend()}/api/exchanges/${id}`)
}

export const list = () => {
  return axios.get(`${getBackend()}/api/exchanges`)
}