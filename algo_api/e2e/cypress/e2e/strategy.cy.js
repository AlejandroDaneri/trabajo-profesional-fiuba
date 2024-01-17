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

    const trade = {
      pair: "BTC",
      amount: "0.5343",
      buy: {
        price: "39000",
        timestamp: 1704844260000,
      },
      sell: {
        price: "40000",
        timestamp: 1704844260000 + 10 * 60 * 1000,
      },
    }

    // creates strategy 1
    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: strategy_1,
    }).then((response) => {
      expect(response.status).to.eq(200)
      // creates trade 1
      cy.request({
        method: "POST",
        url: "/api/trade",
        body: trade,
      }).then((_) => {
        // creates trade 2
        cy.request({
          method: "POST",
          url: "/api/trade",
          body: trade,
        }).then((response) => {
          const strategyID = response.data
          cy.request({
            method: "PUT",
            url: `/api/strategy/stop/${strategyID}`,
          }).then((_) => {
            // creates estrategia 2
            cy.request({
              method: "POST",
              url: "/api/strategy",
              body: strategy_2,
            }).then((_) => {
              // creates trade 1
              cy.request({
                method: "POST",
                url: "/api/trade",
                body: trade,
              }).then((_) => {
                // creates trade 2
                cy.request({
                  method: "POST",
                  url: "/api/trade",
                  body: trade,
                })
              })
            })
          })
        })
      })
    })
  })
})
