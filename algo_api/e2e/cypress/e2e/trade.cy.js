describe("Trade ", () => {

  before(() => {
    // we need create a strategy before crate trades
    // since trades created are associated with running strategy
    const strategy = {
      indicators: [
        {
          name: "rsi",
          parameters: {
            buy_threshold: 65,
            sell_threshold: 55,
            rounds: 14,
          },
        },
      ],
      currencies: ["SOL", "BTC"],
      initial_balance: "1000",
    }
      cy.request({
        method: "POST",
        url: "/api/strategy",
        body: strategy,
      }).then((response) => {
        expect(response.status).to.eq(200)
      })
  })

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
