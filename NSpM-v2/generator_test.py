#!/usr/bin/env python
"""

Neural SPARQL Machines - Generator test unit.

'SPARQL as a Foreign Language' by Tommaso Soru and Edgard Marx et al., SEMANTiCS 2017
https://w3id.org/neural-sparql-machines/soru-marx-semantics2017.html
https://arxiv.org/abs/1708.07624

Version 0.1.0-akaha

"""
import operator

import generator
import generator_utils


def test_extract_variables():
    print ".......Test_Extract_Variables......."
    query = 'select ?a where { <A> bksport:hasAbstract ?a }'

    result = generator_utils.extract_variables(query)
    print query, result


def test_single_resource_sort():
    print ".......Test_Single_Resource_Sort......."

    matches = [{'usages': [17]}, {'usages': [0]}, {'usages': [3]}, {'usages': [2]}, {'usages': [1]}]

    result = sorted(matches, key=generator.prioritize_usage)

    assert map(operator.itemgetter(0), map(operator.itemgetter('usages'), result)) == [17, 3, 2, 1, 0]


def test_couple_resource_sort():
    print ".......Test_Couple_Resource_Sort......."

    matches = [{'usages': [17, 2]}, {'usages': [0, 0]}, {'usages': [3, 2]}, {'usages': [2, 2]}, {'usages': [1, 2]}]

    result = sorted(matches, key=generator.prioritize_usage)

    assert map(operator.itemgetter('usages'), result) == [[17, 2], [3, 2], [2, 2], [1, 2], [0, 0]]


def test_encoding():
    print ".......Test_Encoding......."
    original = 'select ?a where { <A> bksport:hasAbstract ?a }'
    result = generator_utils.encode(original)
    print "Origin:{} Result:{}".format(result, str.strip(generator_utils.decode(result)))


def test_shorten_query():
    print ".......Test_Shorten_Query......."
    shorten = generator_utils.shorten_query
    print "Origin:{} Result:{}".format("ORDER BY var_area", shorten('ORDER BY var_area'))
    print "Origin:{} Result:{}".format("order by asc par_open var_area par_close",
                                       shorten('order by asc par_open var_area par_close'))
    print "Origin:{} Result:{}".format("order by desc attr_open var_area attr_close",
                                       shorten('order by desc attr_open var_area attr_close'))


def test_normalize_predicates():
    print ".......Test_Normalize_Predicates......."
    alt = 'dbp_placeOfBirth'
    print "Origin:{} Result:{}".format(alt, generator_utils.normalize_predicates(alt))


test_extract_variables()
test_encoding()
test_shorten_query()
test_normalize_predicates()
