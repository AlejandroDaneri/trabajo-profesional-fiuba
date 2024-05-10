export const getBackend = () => {
    return process.env.NODE_ENV === "development"
      ? ""
      : "https://api.satoshibot.tech"
}