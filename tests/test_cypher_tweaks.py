from typing import Callable

from transpiler.cypher_generator import CypherGenerator
from transpiler.parser import SelectSparqlParser
from transpiler.structures.nodes import Namespace, Triple


def test_gen_case_prop_var_uri_var(cypher_gen: CypherGenerator):
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    triple = Triple(subject="?s", predicate="abbrev:partOf", object="?o")
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert (
        where_clause
        == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "partOf" '
    )


def test_gen_case_prop_var_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="?o")
    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == ""


def test_gen_case_prop_var_uri_lit(cypher_gen: CypherGenerator):
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    triple = Triple(subject="?s", predicate="abbrev:partOf", object="BR")
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert (
        where_clause
        == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "partOf" AND s[key] = "BR" '
    )


def test_gen_case_prop_var_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="BR")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == 'WHERE s[key] = "BR" '


def test_gen_case_prop(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="?o")
    case_prop = cypher_gen.case_property(triple)

    assert case_prop == "[key in keys(s) | [s, key, s[key]]]"


def test_gen_all_case_prop_all_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="?o")
    case_prop = cypher_gen.case_property(triple)

    assert case_prop == "[key in keys(s) | [s, key, s[key]]]"


def test_gen_all_case_prop_var_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="rdfs:label", object="?o")
    case_prop = cypher_gen.case_property(triple)
    namespaces = [Namespace(abbrev="rdfs", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    assert (
        case_prop
        == '[key in keys(s) WHERE key = n10s.rdf.shortFormFromFullUri("full") + "label" | [s, key, s[key]]]'
    )
