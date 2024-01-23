describe('Ping Tests', () => {
    it('Should return status code 200 and pong for /ping', () => {
      cy.request('GET', '/ping').then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body).to.eq('"pong"')
      })
    })
})
