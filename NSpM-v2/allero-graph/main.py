# coding=utf-8
from franz.openrdf.repository import Repository
from franz.openrdf.sail import AllegroGraphServer

SELECT = 0
ASK = 1
CONSTRUCT_DESCRIBE = 2
ORTHER = 3

def main():
    server = AllegroGraphServer(host="http://107.172.66.48", port=10035,
                                user="bksport", password="bksport@123")
    print(server.listCatalogs())
    #
    catalog = server.openCatalog('vtio-catalog')
    print(catalog.listRepositories())
    #
    with catalog.getRepository("bksport-repository", Repository.ACCESS) as repo:
        with repo.getConnection() as conn:
            query = 'select distinct ?a ?b ?la ?lb where { ?a bksport:defeat ?b . ?a rdfs:label ?la . ?b rdfs:label ?lb }'
            print query
            if checkQueryType(query) == SELECT:
                print query
                tupleQuery = conn.prepareTupleQuery(query=query, baseURI=None)
                tupleQuery.setIncludeInferred(True)

                with tupleQuery.evaluate() as results:
                    for result in results:
                        print(result)
                print(tupleQuery.evaluate_generic_query(count=True))
            elif checkQueryType(query) == ASK:
                booleanQuery = conn.prepareBooleanQuery(query=query)
                booleanQuery.setIncludeInferred(True)
                print booleanQuery.evaluate_generic_query()


def checkQueryType(query):
    type = query.split()[0]
    if type.lower() == "select":
        return SELECT
    elif type.lower() == "ask":
        return ASK
    elif type.lower() == "construct" or type.lower() == "describe":
        return CONSTRUCT_DESCRIBE
    else:
        return ORTHER


if __name__ == '__main__':
    main()
