import argparse

import pandas as pd
from franz.openrdf.repository import Repository
from franz.openrdf.sail import AllegroGraphServer

def main():
    columns = ['id', 'question', 'query', 'generate_query', 'xml', 'csv', 'count']
    datas = pd.read_csv(input, names=columns)
    server = AllegroGraphServer(host=host, port=port,
                                user=username, password=password)
    print(server.listCatalogs())
    #
    catalog = server.openCatalog(cata)
    print(catalog.listRepositories())
    #
    with catalog.getRepository(repository, Repository.ACCESS) as repo:
        with repo.getConnection() as conn:
            counts = []
            for i in range(len(datas)):
                generate_query = datas['generate_query'][i]
                if pd.isnull(generate_query):
                    count = 0
                else:
                    tupleQuery = conn.prepareTupleQuery(query=generate_query)
                    tupleQuery.setIncludeInferred(True)

                    # results = tupleQuery.evaluate()
                    # for result in results:
                    #     print len(result)

                    print generate_query
                    count = tupleQuery.evaluate_generic_query(count=True)
                print count
                counts.append(count)
            print counts
            update_df = pd.DataFrame({'count': counts})
            datas.update(update_df)
            print datas
            datas.to_csv(input, index=False, header=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-ho", "--host", default="http://107.172.66.48",
                    help="Host url")
    ap.add_argument("-p", "--port", default="10035",
                    help="Port")
    ap.add_argument("-u", "--user", default="bksport", help="User name")
    ap.add_argument("-pa", "--password", default="bksport@123", help="Password")
    ap.add_argument("-c", "--catalog", default="vtio-catalog", help="Catalog")
    ap.add_argument("-r", "--repository", default="bksport-repository", help="Repository")
    ap.add_argument("-i", "--input", help="Input file")
    args = ap.parse_args()

    host = args.host
    port = args.port
    username = args.user
    password = args.password

    cata = args.catalog
    repository = args.repository
    input = args.input

    main()
