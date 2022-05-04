import pytest

from transpiler.cypher_generator import CypherGenerator


def test_code_all_var_0(cypher_gen: CypherGenerator):
    query = cypher_gen.parse_query('SELECT ?s WHERE { ?s ?p ?o}')

    pattern = query.mandatory

    cypher_query = cypher_gen.code_block_for_pattern(pattern, query)

    answer = 'MATCH (s)' + '\n' + \
        'UNWIND [key in keys(s) | [s, key, s[key]]] + [(s)-[_relation]-(o) | [s, _relation, o]] AS triples' + '\n' + \
        'WITH triples[0] AS s, triples[1] AS p, triples[2] AS o' + '\n' + \
        'RETURN s'
    assert cypher_query == answer


def test_code_all_var_1(cypher_gen: CypherGenerator):
    query = cypher_gen.parse_query('SELECT * WHERE { ?s ?p ?o}')

    pattern = query.mandatory

    cypher_query = cypher_gen.code_block_for_pattern(pattern, query)

    answer = 'MATCH (s)' + '\n' + \
        'UNWIND [key in keys(s) | [s, key, s[key]]] + [(s)-[_relation]-(o) | [s, _relation, o]] AS triples' + '\n' + \
        'WITH triples[0] AS s, triples[1] AS p, triples[2] AS o' + '\n' + \
        'RETURN *'
    assert cypher_query == answer


def test_code_all_var_2(cypher_gen: CypherGenerator):
    query = cypher_gen.parse_query('SELECT * WHERE { ?s ?p1 ?o1. ?s ?p2 ?o2 }')

    pattern = query.mandatory

    cypher_query = cypher_gen.code_block_for_pattern(pattern, query)

    answer = 'MATCH (s)' + '\n' + \
        'UNWIND [key in keys(s) | [s, key, s[key]]] + [(s)-[_relation]-(o1) | [s, _relation, o1]] AS triples' + '\n' + \
        'WITH triples[0] AS s, triples[1] AS p1, triples[2] AS o1' + '\n' + \
        'UNWIND [key in keys(s) | [s, key, s[key]]] + [(s)-[_relation]-(o2) | [s, _relation, o2]] AS triples' + '\n' + \
        'WITH p1 AS p1, o1 AS o1, triples[0] AS s, triples[1] AS p2, triples[2] AS o2' + '\n' + \
        'RETURN *'
    assert cypher_query == answer
