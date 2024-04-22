import axios from "axios"
import { getBackend } from "./trade"

export const get = (params) => {
    return axios.get(`${getBackend()}/api/backtesting`, {
        params
    })
}