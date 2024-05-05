import axios from "axios";
import { getBackend } from "./trade";

export const add = (exchange) => {
  return axios.post(`${getBackend()}/api/exchanges`, exchange);
};
