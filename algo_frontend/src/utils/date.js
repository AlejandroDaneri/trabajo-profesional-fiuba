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
  const end = end_ || Date.now() / 1000;
  const duration = end - start;
  const days = Math.floor(duration / (60 * 60 * 24));

  if (days > 0) {
    return `${days} days`
  } else {
    const hours = Math.floor(duration / (60 * 60))
    if (hours > 0) {
      return `${hours} hours`
    } else {
      const minutes = Math.floor(duration / 60)
      if (minutes > 0) {
        return `${minutes} minutes`
      } else {
        const seconds = Math.floor(duration);
        return `${seconds} seconds`
      }
    }
  }
}
