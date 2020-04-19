const express = require('express');
const bodyParser = require('body-parser');
const NspmQuestionService = require('./services/NsmpQuestionService');
const DBpediaSparqlClient = require('./services/DBpediaSparqlClient');
const SparqlResponseService = require('./services/SparqlResponseService');
const { BKSportSparqlClient } = require('./services/BKSportSparqlClient');
const app = express();


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

function getPreferredLanguage(req) {
    return req.body.preferredLanguage !== undefined ? req.body.preferredLanguage : 'en';
}

app.post('/nspm', async (req, res) => {
    let nspmQuestionService = new NspmQuestionService();
    let sparqlResponseService = new SparqlResponseService();
    let bksportSparqlClient = new BKSportSparqlClient('bksport', 'bksport@123');
    let sparqlQuery = nspmQuestionService.getSparqlQuery(req.body.question);

    try {
        let response = await bksportSparqlClient.query('catalogs/vtio-catalog/repositories/bksport-repository', sparqlQuery)
        if (typeof response === "boolean") {
            data = {
                boolean: response
            }
        } else {
            data = {
                value: response.values[0][0]
            }
        }
        let result = sparqlResponseService.responseSuccess(data, getPreferredLanguage(req), sparqlQuery)
        console.log({ result })
        res.status(200).json(result);
    }
    catch (error) {
        res.status(500).json(sparqlResponseService.responseError(sparqlQuery));
        console.log("Error")
    }

});

app.post('/sparql', async (req, res) => {
    let bksportSparqlClient = new BKSportSparqlClient('bksport', 'bksport@123');
    let sparqlResponseService = new SparqlResponseService();

    try {
        let response = await bksportSparqlClient.query('catalogs/vtio-catalog/repositories/bksport-repository', req.body.question)
        // console.log(typeof response)
        // console.log(response.values)
        if (typeof response === "boolean") {
            data = {
                boolean: response
            }
        } else {
            data = {
                value: response.values[0][0]
            }
        }
        let result = sparqlResponseService.responseSuccess(data, getPreferredLanguage(req), req.body.question)
        console.log({ result })
        res.status(200).json(result);
    }
    catch (error) {
        res.status(500).json(sparqlResponseService.responseError(req.body.question));
        console.log("Error")
    }

});

app.post('/nspm_training_data', (req, res) => {
    let nspmQuestionService = new NspmQuestionService();
    if (req.body.question === undefined || req.body.query === undefined) {
        res.status(400).json({ error: "question and query parameter required" });
        return;
    }
    nspmQuestionService.addTrainingData(req.body.question, req.body.query);
    res.status(200).json({});
});

const server = app.listen(process.env.PORT || 5000, () => {
    console.log('Express server listening on port %d in %s mode', server.address().port, app.settings.env);
});
