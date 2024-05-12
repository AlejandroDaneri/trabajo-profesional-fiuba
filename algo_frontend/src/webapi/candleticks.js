import axios from "axios"
import { getBackend } from "./env"

export const get = (params) => {
  return axios.get(`${getBackend()}/api/candleticks`, {
    params,
  })
}
