"""Test cases for Cypher code generation from triples assuming that """
from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes import Namespace, Triple

# Where cause for block


def test_gen_where_case_prop_var_var_var(cypher_gen: CypherGenerator):
    """In case the subject and object are variables, no filter shall be applied"""
    triple = Triple(subject="?s", predicate="?p", object="?o")
    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_prop_var_var_lit(cypher_gen: CypherGenerator):
    """If the object is a literal, it shall be used as filter for the property value in the node"""
    triple = Triple(subject="?s", predicate="?p", object="BR")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == 'WHERE s[key] = "BR" '


def test_gen_where_case_prop_var_var_uri(cypher_gen: CypherGenerator):
    """If object is a URI, no where clause is needed because the triple is not a property"""
    triple = Triple(subject="?s", predicate="?p", object="abbrev:any")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_prop_var_uri_var(cypher_gen: CypherGenerator):
    """If the predicate is a URI, the key name shall be used to filter"""
    triple = Triple(subject="?s", predicate="abbrev:partOf", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert (
        where_clause == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "partOf" '
    )


def test_gen_where_case_prop_var_uri_lit(cypher_gen: CypherGenerator):
    """If the predicate is a URI and object a literal, both shall be used as filters"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    triple = Triple(subject="?s", predicate="abbrev:partOf", object="BR")
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert (
        where_clause
        == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "partOf" AND s[key] = "BR" '
    )


def test_gen_where_case_prop_uri_var_var(cypher_gen: CypherGenerator):
    """In case the subject and object are variables, no filter shall be applied"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    triple = Triple(subject="abbrev:uri", predicate="?var", object="?var")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_prop_uri_var_lit(cypher_gen: CypherGenerator):
    """If the object is a literal, it shall be used as filter for the property value in the node"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    triple = Triple(subject="abbrev:uri", predicate="?var", object="lit")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == 'WHERE abbrev_uri[key] = "lit" '


def test_gen_where_case_prop_uri_var_uri(cypher_gen: CypherGenerator):
    """If the object is a URI, no filter is needed because the triple is not a property"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    triple = Triple(subject="abbrev:uri", predicate="?var", object="abbrev:uri")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_prop_uri_uri_var(cypher_gen: CypherGenerator):
    """If predicate is a URI, it shall be used to filter the key value"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    triple = Triple(subject="abbrev:uri", predicate="abbrev:uri", object="?var")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "uri" '


def test_gen_where_case_prop_uri_uri_lit(cypher_gen: CypherGenerator):
    """If the predicate is a URI and object a literal, both shall be used as filters"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    triple = Triple(subject="abbrev:uri", predicate="abbrev:uri", object="lit")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert (
        where_clause
        == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "uri" AND abbrev_uri[key] = "lit" '
    )


def test_gen_where_case_prop_uri_uri_uri(cypher_gen: CypherGenerator):
    """If object is a URI, no filter is necessary because the triple is not a property"""
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    triple = Triple(subject="abbrev:uri", predicate="abbrev:uri", object="abbrev:uri")

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert where_clause == ""


# Full clock generation


def test_gen_all_case_prop_var_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="?o")
    case_prop = cypher_gen.filter_case_property(triple)

    assert case_prop == "[key in keys(s) | [s, key, s[key]]]"


def test_gen_all_case_prop_var_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="Little Label")
    namespaces = [Namespace(abbrev="rdfs", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert (
        case_prop == '[key in keys(s) WHERE s[key] = "Little Label" | [s, key, s[key]]]'
    )


def test_gen_all_case_prop_var_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="rdfs:bla")
    namespaces = [Namespace(abbrev="rdfs", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert case_prop is None


def test_gen_all_case_prop_var_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="rdfs:label", object="?o")
    namespaces = [Namespace(abbrev="rdfs", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert (
        case_prop
        == '[key in keys(s) WHERE key = n10s.rdf.shortFormFromFullUri("full") + "label" | [s, key, s[key]]]'
    )


def test_gen_all_case_prop_var_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="rdfs:label", object="Little Label")
    namespaces = [Namespace(abbrev="rdfs", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert (
        case_prop
        == '[key in keys(s) WHERE key = n10s.rdf.shortFormFromFullUri("full") + "label" AND s[key] = "Little Label" | [s, key, s[key]]]'
    )


def test_gen_all_case_prop_var_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="rdfs:label", object="bla:blu")
    namespaces = [
        Namespace(abbrev="rdfs", full="full"),
        Namespace(abbrev="bla", full="fullbla"),
    ]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert case_prop is None


def test_gen_all_case_prop_uri_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="place:BR", predicate="?p", object="?o")
    namespaces = [Namespace(abbrev="place", full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert case_prop == "[key in keys(place_BR) | [place_BR, key, place_BR[key]]]"


def test_gen_all_case_prop_uri_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="place:BR", predicate="?p", object="Literally")
    namespaces = [Namespace(abbrev="place", full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert (
        case_prop
        == '[key in keys(place_BR) WHERE place_BR[key] = "Literally" | [place_BR, key, place_BR[key]]]'
    )


def test_gen_all_case_prop_uri_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="place:BR", predicate="?p", object="place:any")
    namespaces = [Namespace(abbrev="place", full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert case_prop is None


def test_gen_all_case_prop_uri_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="place:BR", predicate="place:part", object="?o")
    namespaces = [Namespace(abbrev="place", full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert (
        case_prop
        == '[key in keys(place_BR) WHERE key = n10s.rdf.shortFormFromFullUri("placefull") + "part" | [place_BR, key, place_BR[key]]]'
    )


def test_gen_all_case_prop_uri_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="place:BR", predicate="place:part", object="Lit")
    namespaces = [Namespace(abbrev="place", full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert (
        case_prop
        == '[key in keys(place_BR) WHERE key = n10s.rdf.shortFormFromFullUri("placefull") + "part" AND place_BR[key] = "Lit" | [place_BR, key, place_BR[key]]]'
    )


def test_gen_all_case_prop_uri_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="place:BR", predicate="place:part", object="place:bla")
    namespaces = [Namespace(abbrev="place", full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    case_prop = cypher_gen.filter_case_property(triple)
    assert case_prop is None
