describe("Strategy ", () => {
  before(() => {
    const strategy_example = {
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

    Cypress.env('strategy_example', strategy_example)

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

  it("State should be created after creation", () => {
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

    // creates strategy
    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: strategy,
    }).then((response) => {
      const strategyID = response.body

      // get strategy
      cy.request({
        method: "GET",
        url: `/api/strategy/${strategyID}`,
      }).then(response => {
        const strategy = JSON.parse(response.body)
        expect(strategy.state).to.eq("created")
      })
    })
  })

  it("State should change to running after set start", () => {
    // creates strategy
    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: Cypress.env('strategy_example'),
    }).then((response) => {
      const strategyID = response.body
      // set state to stop
      cy.request({
        method: "PUT",
        url: `/api/strategy/${strategyID}/stop`,
      }).then(response => {
        // get strategy
        cy.request({
          method: "GET",
          url: `/api/strategy/${strategyID}`,
        }).then(response => {
          const strategy = JSON.parse(response.body)
          expect(strategy.state).to.eq("finished")
        })
      })
    })
  })

  it("State should change to finished after set stop", () => {
    // creates strategy
    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: Cypress.env('strategy_example'),
    }).then((response) => {
      const strategyID = response.body

      // set state to start
      cy.request({
        method: "PUT",
        url: `/api/strategy/${strategyID}/start`,
      }).then(response => {
        // get strategy
        cy.request({
          method: "GET",
          url: `/api/strategy/${strategyID}`,
        }).then(response => {
          const strategy = JSON.parse(response.body)
          expect(strategy.state).to.eq("running")
        })
      })
    })
  })
})
