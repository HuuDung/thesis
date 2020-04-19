"use strict";

const fs = require('fs');

module.exports = class NspmQuestionService {

    getSparqlQuery(question) {
        let shell = require('shelljs');
        let nspmResult = shell.exec('cd ../NSpM/ && sh ask.sh data-v1/data "' + question + '"').stdout;
        return nspmResult.substring(nspmResult.lastIndexOf("ANSWER IN SPARQL SEQUENCE:") + 27);
    }

    addTrainingData(question, query) {

        if (!fs.existsSync('../NSpM/data-v1/collected_training_data')) {
            fs.mkdirSync('../NSpM/data-v1/collected_training_data');
        }
        fs.appendFile(
            '../NSpM/data-v1/collected_training_data/training_data.ensparql',
            question + ' | ' + query + '\n'
        );
    }
};