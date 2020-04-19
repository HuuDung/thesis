const http = require('request-promise')
const crypto = require('crypto')
// const shasum = crypto.createHash('sha1')

class BKSportSparqlClient {

    getCookie(username, password) {
        return `auth4=bksport: ${require('crypto').createHash('sha1').update(`agraph:${username}:${password}`).digest('hex')}`
    }

    constructor(username, password) {
        const Cookie = this.getCookie(username, password)
        this.client = http.defaults({
            baseUrl: 'http://107.172.66.48:10035',
            headers: {
                Cookie,
                'X-Cookie-Auth': 'yes'
            },
            json: true
        })
    }

    query(url, query) {
        let qs = { 
            query: query,
            infer: true,
            limit: 1,
            queryLn: 'SPARQL',
        }
        return this.client(url, { qs })
    }
}


module.exports = {
    BKSportSparqlClient,
};