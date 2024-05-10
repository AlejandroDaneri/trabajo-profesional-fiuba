import axios from "axios";
import { getBackend } from "./env"

export const add = (exchange) => {
  return axios.post(`${getBackend()}/api/exchanges`, exchange);
};

export const remove = (exchange) => {
  return axios.delete(`${getBackend()}/api/exchanges`, { data: exchange });
}

export const get = () => {
  return axios.get(`${getBackend()}/api/exchanges`)
}