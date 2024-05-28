describe("Strategy", () => {
  before(() => {

    cy.request({
      method: "DELETE",
      url: "/api/exchanges/all"
    }).then(_ => {

      cy.request({
        method: "DELETE",
        url: "/api/strategy/all"
      }).then(_ => {

        const exchange = {
          api_key: "QexP3dpD7YnrVnnDZQhIISuImLfMbhoh9BgkKxQzNtPY6rEVC4WIBkVd2g3yxipc",
          api_secret: "RxrSIf1F8vj34scJ3MTJkqJvwmIQUZKUOiYGcuukU83t0W9e8RsxSNj0sY8y3XOr",
          alias: "binance_test",
          testing_network: true,
          exchange_name: "binance"
        }

        cy.request({
          method: "POST",
          url: "/api/exchanges",
          body: exchange
        }).then((response) => {

          const exchangeId = response.body

          const strategy = {
            indicators: [
              {
                name: "RSI",
                parameters: {
                  buy_threshold: 65,
                  sell_threshold: 55,
                  rounds: 14,
                },
              },
            ],
            exchange_id: exchangeId,
            currencies: ["BTC"],
            initial_balance: "1000",
            type: "basic",
            timeframe: '5m'
          }
    
          Cypress.env('strategy_example', strategy)
        })
      })
    })
  })

  it("Should get trade after create it", () => {
    // create strategy
    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: Cypress.env('strategy_example'),
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
    // creates strategy
    cy.request({
      method: "POST",
      url: "/api/strategy",
      body: Cypress.env('strategy_example'),
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
      const strategyId = response.body
      // set state to start
      cy.request({
        method: "PUT",
        url: `/api/strategy/${strategyId}/start`,
      }).then(response => {
        expect(response.status).to.eq(200)

        // get strategy
        cy.request({
          method: "GET",
          url: `/api/strategy/${strategyId}`,
        }).then(response => {
          expect(response.status).to.eq(200)

          const strategy = JSON.parse(response.body)
          expect(strategy.state).to.eq("running")
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
})
