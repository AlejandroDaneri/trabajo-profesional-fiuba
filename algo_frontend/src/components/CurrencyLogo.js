/* Import Libs */
import styled from "styled-components"

/* Import Images */
import btc from "../images/logos/btc.png"
import sol from "../images/logos/sol.png"
import eth from "../images/logos/eth.png"

const CurrencyLogoStyle = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;

  & img {
    width: 24px;
    height: 24px;
    border-radius: 30px;
  }
`

const CurrencyLogo = ({ currency }) => {
  return (
    <CurrencyLogoStyle>
      {(() => {
        switch (currency) {
          case "BTC":
            return <img src={btc} alt="logo" />
          case "SOL":
            return <img src={sol} alt="logo" />
          case "ETH":
            return <img src={eth} alt="logo" />
          default:
            return <></>
        }
      })()}
    </CurrencyLogoStyle>
  )
}

export default CurrencyLogo
