export const unixToDate = (unix) => {
  const date = new Date(unix)

  const yyyy = date.getFullYear()
  const MM = date.getMonth()
  const dd = padding(date.getDate())
  const hh = padding(date.getHours())
  const mm = padding(date.getMinutes())
  const ss = padding(date.getSeconds())

  return `${yyyy}-${MM}-${dd} ${hh}:${mm}:${ss}`
}

export const padding = (n) => {
  return String(n).padStart(2, "0")
}
