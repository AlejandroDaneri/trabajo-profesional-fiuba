describe("Get ", () => {
  it("Should get trade after create it", () => {
    const trade = {
      pair: "BTC/USDT",
      price: "39000",
      amount: "0.5343",
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
        expect(trade.price).eq("39000")
        expect(trade.amount).eq("0.5343")
      })
    })
  })
})
