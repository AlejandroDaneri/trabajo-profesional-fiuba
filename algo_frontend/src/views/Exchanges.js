/* Import Libs */
import React from 'react'
import styled from 'styled-components'

/* Import Reusables Components */
import View from '../components/reusables/View'

const ExchangesStyle = styled.div`
`

const Exchanges = () => {
    return (
        <>
            <View
                title="Exchanges"
                content={
                    <ExchangesStyle>
                    </ExchangesStyle>
                }
            />
        </>
    )
}

export default Exchanges