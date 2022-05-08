"""Test cases for Cypher code generation of the with clause that comes after each triple filter block"""

from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes import Triple
from transpiler.structures.nodes.namespace import Namespace


def test_match_var_any_any(cypher_gen: CypherGenerator):
    """If the subject is a variable, the match statment don't need a where"""
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    triples = [
        Triple(subject="?var", predicate="?var", object="?var"),
        Triple(subject="?var", predicate="?var", object="lit"),
        Triple(subject="?var", predicate="?var", object="abbrev:uri"),
        Triple(subject="?var", predicate="abbrev:uri", object="?var"),
        Triple(subject="?var", predicate="abbrev:uri", object="lit"),
        Triple(subject="?var", predicate="abbrev:uri", object="abbrev:uri"),
    ]

    for triple in triples:
        match = cypher_gen.match_clause(triple)

        assert match == "MATCH (var)"


def test_match_uri_any_any(cypher_gen: CypherGenerator):
    """Is the subject is a uri, the match statment should filter by its uri value using where"""
    triples = [
        Triple(subject="abbrev:uri", predicate="?var", object="?var"),
        Triple(subject="abbrev:uri", predicate="?var", object="lit"),
        Triple(subject="abbrev:uri", predicate="?var", object="abbrev:uri"),
        Triple(subject="abbrev:uri", predicate="abbrev:uri", object="?var"),
        Triple(subject="abbrev:uri", predicate="abbrev:uri", object="lit"),
        Triple(
            subject="abbrev:uri", predicate="abbrev:uri", object="abbrev:uri"
        ),
    ]

    for triple in triples:
        namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
        cypher_gen.setup_namespaces(namespaces)
        match = cypher_gen.match_clause(triple)

        assert (
            match
            == 'MATCH (abbrev_uri) WHERE abbrev_uri.uri = "abbrevfulluri"'
        )


def test_match_var_reused(cypher_gen: CypherGenerator):
    """There is no need to match a variable that was already used"""
    triples = [
        Triple(subject="?s", predicate="?var", object="?var"),
        Triple(subject="?s", predicate="?var", object="lit"),
    ]

    cypher_gen.match_clause(triples[0])
    cypher_gen.with_clause(triples[0])

    match = cypher_gen.match_clause(triples[1])

    assert not match
