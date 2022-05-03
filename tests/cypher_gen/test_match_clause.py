"""Test cases for Cypher code generation of the with clause that comes after each triple filter block"""

from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes import Triple
from transpiler.structures.nodes.namespace import Namespace


def test_match_var_any_any(cypher_gen: CypherGenerator):
    namespaces = [Namespace(abbrev='abbrev', full='abbrevfull')]
    cypher_gen.setup_namespaces(namespaces)

    triples = [
        Triple(subject='?var', predicate='?var', object='?var'),
        Triple(subject='?var', predicate='?var', object='lit'),
        Triple(subject='?var', predicate='?var', object='abbrev:uri'),
        Triple(subject='?var', predicate='abbrev:uri', object='?var'),
        Triple(subject='?var', predicate='abbrev:uri', object='lit'),
        Triple(subject='?var', predicate='abbrev:uri', object='abbrev:uri'),
    ]

    for triple in triples:
        match = cypher_gen.match_clause(triple)

        assert match == 'MATCH (var)'


def test_match_uri_any_any(cypher_gen: CypherGenerator):
    triples = [
        Triple(subject='abbrev:uri', predicate='?var', object='?var'),
        Triple(subject='abbrev:uri', predicate='?var', object='lit'),
        Triple(subject='abbrev:uri', predicate='?var', object='abbrev:uri'),
        Triple(subject='abbrev:uri', predicate='abbrev:uri', object='?var'),
        Triple(subject='abbrev:uri', predicate='abbrev:uri', object='lit'),
        Triple(subject='abbrev:uri', predicate='abbrev:uri', object='abbrev:uri'),
    ]

    for triple in triples:
        namespaces = [Namespace(abbrev='abbrev', full='abbrevfull')]
        cypher_gen.setup_namespaces(namespaces)
        match = cypher_gen.match_clause(triple)

        assert match == 'MATCH (abbrev_uri) WHERE abbrev_uri.uri = n10s.rdf.shortFormFromFullUri("abbrevfull") + "uri"'