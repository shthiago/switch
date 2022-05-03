"""Test cases for Cypher code generation of the with clause that comes after each triple filter block"""

from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes import Triple


def test_with_clause_var_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='?p', object='?o')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[0] AS s, triples[1] AS p, triples[2] AS o'


def test_with_clause_var_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='?p', object='lit')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[0] AS s, triples[1] AS p'


def test_with_clause_var_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='?p', object='abbrev:uri')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[0] AS s, triples[1] AS p'


def test_with_clause_var_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='abbrev:uri', object='?o')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[0] AS s, triples[2] AS o'


def test_with_clause_var_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='abbrev:uri', object='lit')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[0] AS s'


def test_with_clause_var_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='abbrev:uri', object='abbrev:uri')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[0] AS s'


def test_with_clause_uri_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject='abbrev:uri', predicate='?p', object='?o')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[1] AS p, triples[2] AS o'


def test_with_clause_uri_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject='abbrev:uri', predicate='?p', object='lit')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[1] AS p'


def test_with_clause_uri_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject='abbrev:uri', predicate='?p', object='abbrev:uri')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[1] AS p'


def test_with_clause_uri_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject='abbrev:uri', predicate='abbrev:uri', object='?o')

    clause = cypher_gen.with_clause(triple)

    assert clause == 'WITH triples[2] AS o'


def test_with_clause_uri_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject='abbrev:uri', predicate='abbrev:uri', object='lit')

    clause = cypher_gen.with_clause(triple)

    assert clause is None


def test_with_clause_uri_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject='abbrev:uri',
                    predicate='abbrev:uri', object='abbrev:uri')

    clause = cypher_gen.with_clause(triple)

    assert clause is None


def test_two_consecutive_triples(cypher_gen: CypherGenerator):
    first_triple = Triple(subject='abbrev:uri',
                          predicate='abbrev:uri', object='?o')
    second_triple = Triple(subject='?s', predicate='abbrev:uri', object='lit')

    first_with = cypher_gen.with_clause(first_triple)

    assert first_with == 'WITH triples[2] AS o'

    second_with = cypher_gen.with_clause(second_triple)

    assert second_with == 'WITH o AS o, triples[0] AS s'


def test_three_consecutive_triples(cypher_gen: CypherGenerator):
    first_triple = Triple(subject='abbrev:uri',
                          predicate='abbrev:uri', object='?o')
    second_triple = Triple(subject='?s', predicate='abbrev:uri', object='lit')
    third_triple = Triple(subject='abbrev:uri',
                          predicate='abbrev:uri', object='abbrev:uri')

    first_with = cypher_gen.with_clause(first_triple)

    assert first_with == 'WITH triples[2] AS o'

    second_with = cypher_gen.with_clause(second_triple)

    assert second_with == 'WITH o AS o, triples[0] AS s'

    third_with = cypher_gen.with_clause(third_triple)

    assert third_with == 'WITH o AS o, s AS s'


def test_four_consecutive_triples(cypher_gen: CypherGenerator):
    first_triple = Triple(subject='abbrev:uri',
                          predicate='abbrev:uri', object='?o')
    second_triple = Triple(subject='?s', predicate='abbrev:uri', object='lit')
    third_triple = Triple(subject='abbrev:uri',
                          predicate='abbrev:uri', object='abbrev:uri')
    forth_triple = Triple(subject='?s',
                          predicate='abbrev:uri', object='abbrev:uri')

    first_with = cypher_gen.with_clause(first_triple)

    assert first_with == 'WITH triples[2] AS o'

    second_with = cypher_gen.with_clause(second_triple)

    assert second_with == 'WITH o AS o, triples[0] AS s'

    third_with = cypher_gen.with_clause(third_triple)

    assert third_with == 'WITH o AS o, s AS s'

    forth_with = cypher_gen.with_clause(forth_triple)

    assert forth_with == 'WITH o AS o, triples[0] AS s'
