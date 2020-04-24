import re

import pandas as pd
from franz.openrdf.repository import Repository
from franz.openrdf.sail import AllegroGraphServer

MAX = 600
FILE_DATA = './annotation_sport.csv'

HOST = "http://107.172.66.48"
PORT = 10035
USERNAME = "bksport"
PASSWORD = "bksport@123"

CATALOG = "vtio-catalog"
REPOSITORY = "bksport-repository"


def modifyLabel(label):
    return re.sub("@en", "", label)


def modifyLabel_v2(label):
    label = re.sub("\"", "", label)
    return re.sub("@en", "", label)


def modifyURI(label):
    tmp = re.sub("<", "", label)
    return re.sub(">", "", tmp)


def checkLabel(label):
    if "\u" in label:
        return False
    else:
        return True


def extract_bindings(filename):
    count = 1
    file = pd.read_csv(filename)
    # print file
    name = [name for name in file]
    # print(name)
    results = []
    if len(name) == 2:
        a = file[name[0]]
        la = file[name[1]]
        for i in range(len(file)):
            if checkLabel(la[i]):
                result = {
                    'a': {
                        'uri': unicode(modifyURI(a[i])),
                        'label': unicode(modifyLabel(la[i])),
                    }
                }
                results.append(result)
                count = count + 1
                if count > MAX:
                    break
    elif len(name) == 4:
        a = file[name[0]]
        b = file[name[1]]
        la = file[name[2]]
        lb = file[name[3]]
        for i in range(len(file)):
            if checkLabel(la[i]) and checkLabel(lb[i]):
                result = {
                    'a': {
                        'uri': unicode(modifyURI(a[i])),
                        'label': unicode(modifyLabel(la[i])),
                    },
                    'b': {
                        'uri': unicode(modifyURI(b[i])),
                        'label': unicode(modifyLabel(lb[i])),
                    }
                }
                # print json.dumps(result, indent=4)

                results.append(result)
                count = count + 1
                if count > MAX:
                    break
    # print json.dumps(results, indent=4)
    # print len(results)
    return results


def read_template_file(file=FILE_DATA):
    annotations = list()
    line_number = 1
    with open(file) as f:
        for line in f:
            values = line[:-1].split(',')
            target_classes = [values[0] or None]
            question = values[1]  # natural language
            query = values[2]  # sparql
            generate_query = values[3]
            id = line_number
            line_number += 1
            file_xml = values[4]
            file_csv = values[5]
            annotation = Annotation(question, query, generate_query, id, target_classes, file_xml, file_csv)
            annotations.append(annotation)
    return annotations


class Annotation:
    def __init__(self, question, query, generate_query, id=None, target_classes=None, file_xml=None, file_csv=None,
                 variables=None):
        self.question = question
        self.query = query
        self.generate_query = generate_query
        self.file_xml = file_xml
        self.file_csv = file_csv
        self.id = id
        self.target_classes = target_classes if target_classes != None else []
        self.variables = variables


def extract_bindings_v2(generate_query, input_host=HOST, input_port=PORT, input_user=USERNAME, input_password=PASSWORD,
                        input_catalog=CATALOG, input_repository=REPOSITORY):
    server = AllegroGraphServer(host=input_host, port=input_port,
                                user=input_user, password=input_password)
    # print(server.listCatalogs())
    #
    catalog = server.openCatalog(input_catalog)
    # print(catalog.listRepositories())
    #
    with catalog.getRepository(input_repository, Repository.ACCESS) as repo:
        with repo.getConnection() as conn:
            results = []
            count = 0
            if generate_query:
                tupleQuery = conn.prepareTupleQuery(query=generate_query)
                tupleQuery.setIncludeInferred(True)
                datas = tupleQuery.evaluate()
                count = tupleQuery.evaluate(count=True)
                for data in datas:
                    if len(data) == 2:
                        result = {
                            'a': {
                                'uri': unicode(modifyURI(str(data['a']))),
                                'label': unicode(modifyLabel_v2(str(data['la'])))
                            }
                        }
                        results.append(result)
                    elif len(data) == 4:
                        result = {
                            'a': {
                                'uri': unicode(modifyURI(str(data['a']))),
                                'label': unicode(modifyLabel_v2(str(data['la'])))
                            }
                            ,
                            'b': {
                                'uri': unicode(modifyURI(str(data['b']))),
                                'label': unicode(modifyLabel_v2(str(data['lb'])))
                            }
                        }
                        results.append(result)
            return results, count
