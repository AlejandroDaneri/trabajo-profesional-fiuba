describe("Strategy ", () => {
  it("Should get trade after create it", () => {
    const strategy_1 = {
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

    const strategy_2 = {
      indicators: [
        {
          name: "crossing",
          parameters: {
            buy_threshold: -0.01,
            sell_threshold: 0,
            fast: 20,
            slow: 60,
          },
        },
      ],
      currencies: ["SOL", "ETH"],
      initial_balance: "1000",
    }

    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: strategy_1,
    }).then((response) => {
      expect(response.status).to.eq(200)
    })

    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: strategy_2,
    }).then((response) => {
      expect(response.status).to.eq(200)
    })
  })
})
