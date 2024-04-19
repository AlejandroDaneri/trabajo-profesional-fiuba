import axios from "axios"
import { getBackend } from "./trade"

export const getBuyAndHold = (params) => {
    return axios.get(`${getBackend()}/api/chart_data/buy_and_hold`, {
        params
    })
}