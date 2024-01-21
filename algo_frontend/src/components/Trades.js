/* Import Libs */
import { useEffect } from "react"
import styled from "styled-components"

/* Import WebApi */
import { list } from "../webapi/trade"

const TradesStyle = styled.div`
  display: flex;
`

const Trades = ({ strategyID }) => {
  useEffect(() => {
    if (strategyID) {
      list(strategyID).then((response) => {
        console.info(response.data)
      })
    }
  }, [strategyID])

  return <TradesStyle></TradesStyle>
}

export default Trades
