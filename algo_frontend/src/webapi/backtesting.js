import axios from "axios"
import { getBackend } from "./env"

export const getIndicators = () => {
    return axios.get(`${getBackend()}/api/indicators`)
}

export const run = (body) => {
    return axios.post(`${getBackend()}/api/backtesting`, body)
}