import axios from "axios";
import { getBackend } from "./env"

export const add = (exchange) => {
  return axios.post(`${getBackend()}/api/exchanges`, exchange)
}

export const edit = (id, exchange) => {
  return axios.put(`${getBackend()}/api/exchanges/${id}`, exchange)
}

export const remove = (id) => {
  return axios.delete(`${getBackend()}/api/exchanges/${id}`)
}

export const get = (id) => {
  return axios.get(`${getBackend()}/api/exchanges/${id}`)
}

export const getBalance = (id) => {
  return axios.get(`${getBackend()}/api/exchanges/${id}/balance`)
}

export const list = () => {
  return axios.get(`${getBackend()}/api/exchanges`)
}