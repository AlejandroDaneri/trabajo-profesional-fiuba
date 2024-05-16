import moment from "moment"

export const unixToDate = (unix) => {
  const date = new Date(unix * 1000)

  const yyyy = date.getFullYear()
  const MM = padding(date.getMonth() + 1)
  const dd = padding(date.getDate())
  const hh = padding(date.getHours())
  const mm = padding(date.getMinutes())

  return `${yyyy}-${MM}-${dd} ${hh}:${mm}`
}

export const padding = (n) => {
  return String(n).padStart(2, "0")
}

export const getDuration = (start, end_) => {
  const end = end_ || Date.now() / 1000
  const days = Math.floor((end - start) / (60 * 60 * 24))
  if (days > 0) {
    return `${days} days`
  } else {
    return moment.utc((end - start) * 1000).format("HH:mm:ss")
  }
}
