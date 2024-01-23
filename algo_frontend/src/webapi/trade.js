import axios from "axios"

export const getBackend = () => {
  return process.env.NODE_ENV === "development"
    ? ""
    : "https://api.satoshibot.tech"
}

export const list = (strategyID) => {
  return axios.get(`${getBackend()}/api/trades/strategy/${strategyID}`)
}
