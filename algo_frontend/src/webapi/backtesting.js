import axios from "axios"
import { getBackend } from "./trade"

export const run = (body) => {
    return axios.post(`${getBackend()}/api/backtesting`, body)
}