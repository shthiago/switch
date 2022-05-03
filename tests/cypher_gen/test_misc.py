from typing import Callable

import pytest

from transpiler.cypher_generator import CypherGenerator, CypherGenerationException
from transpiler.parser import SelectSparqlParser, Query
from transpiler.structures.nodes import Namespace, Triple, namespace


def test_gen_var_for_var(cypher_gen: CypherGenerator):
    assert cypher_gen.cypher_var_for('?var') == 'var'


def test_gen_var_for_uri_0(cypher_gen: CypherGenerator):
    assert cypher_gen.cypher_var_for('p:p') == 'p_p'


def test_gen_var_for_uri_1(cypher_gen: CypherGenerator):
    assert cypher_gen.cypher_var_for(':p') == '_p'


def test_gen_var_for_lit_0(cypher_gen: CypherGenerator):
    with pytest.raises(CypherGenerationException):
        cypher_gen.cypher_var_for('1')


def test_gen_var_for_lit_1(cypher_gen: CypherGenerator):
    with pytest.raises(CypherGenerationException):
        cypher_gen.cypher_var_for(1)


def test_return_clause_0(cypher_gen: CypherGenerator):
    query = cypher_gen.parse_query('SELECT ?s WHERE { ?s ?p ?o }')

    clause = cypher_gen.return_clause(query)

    assert clause == 'RETURN s'

def test_return_clause_1(cypher_gen: CypherGenerator):
    query = cypher_gen.parse_query('SELECT ?s ?o WHERE { ?s ?p ?o }')

    clause = cypher_gen.return_clause(query)

    assert clause == 'RETURN s, o'


def test_return_clause_2(cypher_gen: CypherGenerator):
    query = cypher_gen.parse_query('SELECT * WHERE { ?s ?p ?o }')

    clause = cypher_gen.return_clause(query)

    assert clause == 'RETURN *'


def test_return_clause_alias(cypher_gen: CypherGenerator):
    query = cypher_gen.parse_query('SELECT ?s WHERE { ?s ?p ?o}')

    clause = cypher_gen.return_clause(query)

    assert clause == 'RETURN s'