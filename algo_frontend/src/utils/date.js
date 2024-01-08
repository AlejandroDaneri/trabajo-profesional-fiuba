export const unixToDate = (unix) => {
  const date = new Date(unix)

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
