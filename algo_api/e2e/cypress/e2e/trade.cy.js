describe("Trade ", () => {
  it("Should get trade after create it", () => {
    const trade = {
      pair: "BTC/USDT",
      amount: "0.5343",
      buy: {
        price: "39000",
        timestamp: 1702831239,
      },
      sell: {
        price: "40000",
        timestamp: 1702831339,
      },
    }

    cy.request({
      method: "POST",
      url: "/api/trade",
      body: trade,
    }).then((response) => {
      expect(response.status).to.eq(200)
      const tradeId = response.body
      expect(tradeId).to.be.a("string").that.is.not.empty

      cy.request({
        method: "GET",
        url: `/api/trade/${tradeId}`,
      }).then((response) => {
        expect(response.status).to.eq(200)
        const trade = JSON.parse(response.body)
        expect(trade.pair).eq("BTC/USDT")
        expect(trade.amount).eq("0.5343")
        expect(trade.orders.buy.price).eq("39000")
        expect(trade.orders.buy.timestamp).eq(1702831239)
        expect(trade.orders.sell.price).eq("40000")
        expect(trade.orders.sell.timestamp).eq(1702831339)
      })
    })
  })
})
