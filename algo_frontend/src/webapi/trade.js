import axios from "axios"

export const list = () => {
  return axios.get("/api/trade")
}
