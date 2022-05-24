import pytest

from transpiler.cypher_generator import CypherGenerationException, CypherGenerator
from transpiler.structures.nodes import Triple
from transpiler.structures.nodes.graph_pattern import GraphPattern
from transpiler.structures.nodes.namespace import Namespace


def test_gen_var_for_var(cypher_gen: CypherGenerator):
    """For a sparql variable, the cypher variable should be it without the ?"""
    assert cypher_gen.cypher_var_for("?var") == "var"


def test_gen_var_for_uri_0(cypher_gen: CypherGenerator):
    """For a sparql prefixed URI, the cypher var should be itself replacing : with _"""
    assert cypher_gen.cypher_var_for("p:p") == "p_p"


def test_gen_var_for_uri_1(cypher_gen: CypherGenerator):
    """For a sparql prefixed URI, the cypher var should be itself replacing : with _"""
    assert cypher_gen.cypher_var_for(":p") == "_p"


def test_gen_var_for_lit_0(cypher_gen: CypherGenerator):
    """There is no variable for literals"""
    with pytest.raises(CypherGenerationException):
        cypher_gen.cypher_var_for("1")


def test_gen_var_for_lit_1(cypher_gen: CypherGenerator):
    """There is no variable for literals"""
    with pytest.raises(CypherGenerationException):
        cypher_gen.cypher_var_for(1)


def test_return_clause_0(cypher_gen: CypherGenerator):
    """The return clause shall imitate the selected variables of sparql on simple cases"""
    query = cypher_gen.parse_query("SELECT ?s WHERE { ?s ?p ?o }")

    clause = cypher_gen.return_clause(query)

    assert clause == "RETURN s"


def test_return_clause_1(cypher_gen: CypherGenerator):
    """The return clause shall imitate the selected variables of sparql on simple cases"""
    query = cypher_gen.parse_query("SELECT ?s ?o WHERE { ?s ?p ?o }")

    clause = cypher_gen.return_clause(query)

    assert clause == "RETURN s, o"


def test_return_clause_2(cypher_gen: CypherGenerator):
    """The return clause shall imitate the selected variables of sparql on simple cases"""
    query = cypher_gen.parse_query("SELECT * WHERE { ?s ?p ?o }")

    clause = cypher_gen.return_clause(query)

    assert clause == "RETURN *"


def test_unroll_or_blocks(cypher_gen: CypherGenerator):
    """The internal graph patterns shall be transformed in a list of GraphPatterns without or_blocks, only and_triples and rest of query"""
    graph = GraphPattern(
        or_blocks=[
            [
                GraphPattern(
                    or_blocks=[
                        [
                            GraphPattern(and_triples=[Triple("?s1", "?p2", "?o")]),
                            GraphPattern(and_triples=[Triple("?s", "?p2", "?o")]),
                        ]
                    ]
                ),
                GraphPattern(and_triples=[Triple("?s", "?p1", "?o")]),
            ]
        ]
    )

    unrolled = cypher_gen.split_pattern(graph)

    assert len(unrolled) == 3


def test_unroll_or_blocks_2(cypher_gen: CypherGenerator):
    """The internal graph patterns shall be transformed in a list of GraphPatterns without or_blocks

    But every block shall be unrolled considering the and_triples as a distributive to or_blocks.

    (triple1 & triple2) & (triple3 or triple4) -> (triple1 & triple2 & triple3) or (triple1 & triple2 & triple4)
    """
    graph = GraphPattern(
        and_triples=[Triple("?s1", "?p1", "?o1"), Triple("?s1", "?p2", "?o2")],
        or_blocks=[
            [
                GraphPattern(
                    or_blocks=[
                        [
                            GraphPattern(and_triples=[Triple("?s1", "?p3", "?o3")]),
                            GraphPattern(and_triples=[Triple("?s1", "?p4", "?o4")]),
                        ]
                    ]
                )
            ]
        ],
    )

    unrolled = cypher_gen.split_pattern(graph)

    assert len(unrolled) == 2

    assert set(unrolled[0].and_triples) == {
        Triple("?s1", "?p1", "?o1"),
        Triple("?s1", "?p2", "?o2"),
        Triple("?s1", "?p3", "?o3"),
    }

    assert set(unrolled[1].and_triples) == {
        Triple("?s1", "?p1", "?o1"),
        Triple("?s1", "?p2", "?o2"),
        Triple("?s1", "?p4", "?o4"),
    }


def test_unwind_clause_0(cypher_gen: CypherGenerator):
    """The unwind clause should be the sum of the cases, when subject and object are variables"""
    triple = Triple(subject="?s", predicate="?p", object="?o")

    unwind = cypher_gen.unwind_clause(triple)

    assert (
        unwind
        == "UNWIND [key in keys(s) | [s, key, s[key]]] + [(s)-[_relation]-(o) | [s, _relation, o]] AS triples"
    )


def test_unwind_clause_1(cypher_gen: CypherGenerator):
    """The unwind clause should cointain only the object case when object is a uri"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)
    triple = Triple(subject="?s", predicate="?p", object="abbrev:uri")

    unwind = cypher_gen.unwind_clause(triple)

    assert (
        unwind
        == 'UNWIND [(s)-[_relation]-(abbrev_uri) WHERE abbrev_uri.uri = "fulluri" | [s, _relation, abbrev_uri]] AS triples'
    )


def test_unwind_clause_2(cypher_gen: CypherGenerator):
    """The unwind clause should contain only the property part whe object is a literal"""
    triple = Triple(subject="?s", predicate="?p", object="literal")

    unwind = cypher_gen.unwind_clause(triple)

    assert (
        unwind
        == 'UNWIND [key in keys(s) WHERE s[key] = "literal" | [s, key, s[key]]] AS triples'
    )


def test_special_match_case(cypher_gen: CypherGenerator):
    """The rdf:type is converted to a Label in Neo4j, so the search is different"""
    namespaces = [Namespace(abbrev="b", full="fullb")]
    triple = Triple(subject="?s", predicate="rdf:type", object="b:Country")

    cypher_gen.setup_namespaces(namespaces)

    code = cypher_gen.match_clause(triple)

    assert (
        code
        == 'MATCH (s) WHERE n10s.rdf.shortFormFromFullUri("fullb") + "Country" IN labels(s)'
    )


def test_special_full_block(cypher_gen: CypherGenerator):
    """The rdf:type is converted to a Label in Neo4j, so the search is different"""
    namespaces = [Namespace(abbrev="b", full="fullb")]
    triple = Triple(subject="?s", predicate="rdf:type", object="b:Country")

    cypher_gen.setup_namespaces(namespaces)

    code = cypher_gen.code_block_for_triple(triple)

    assert (
        code
        == 'MATCH (s) WHERE n10s.rdf.shortFormFromFullUri("fullb") + "Country" IN labels(s)\nWITH s AS s'
    )
