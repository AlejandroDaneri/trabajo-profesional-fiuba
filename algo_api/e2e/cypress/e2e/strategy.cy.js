describe("Strategy ", () => {
  before(() => {
    cy.request({
      method: "DELETE",
      url: "/api/strategy",
    }).then((response) => {
      expect(response.status).to.be.oneOf([200])
    })

    cy.request({
      method: "DELETE",
      url: "/api/trade",
    }).then((response) => {
      expect(response.status).to.be.oneOf([200])
    })
  })

  it("Should get trade after create it", () => {
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

    // create strategy
    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: strategy,
    }).then((response) => {
      const strategyID = response.body
      expect(response.status).to.eq(200)
      expect(strategyID).to.be.a('string')
      expect(strategyID).to.not.be.empty

      // get strategy
      cy.request({
        method: "GET",
        url: `/api/strategy/${strategyID}`,
      }).then(response => {
        expect(JSON.parse(response.body).id).to.eq(strategyID)
      })
    })
  })
})
