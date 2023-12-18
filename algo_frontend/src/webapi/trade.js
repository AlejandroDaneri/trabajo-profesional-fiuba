import axios from "axios"

export const getBackend = () => {
  return process.env.NODE_ENV === "development"
    ? ""
    : "http://satoshibot.tech:8080"
}

export const list = () => {
  return axios.get(`${getBackend()}/api/trade`)
}
