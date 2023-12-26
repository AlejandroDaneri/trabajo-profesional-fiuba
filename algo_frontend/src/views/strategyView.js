/* Import Libs */
import React from "react"
import StrategyStyle from "../styles/strategy"
import { useEffect } from "react"
import { getStrategy } from "../webapi/strategy"

const StrategyView = () => {
  useEffect(() => {
    getStrategy()
      .then((_) => {
        console.info("ok")
      })
      .catch((_) => {})
  }, [])

  return <StrategyStyle>Strategy</StrategyStyle>
}

export default StrategyView
