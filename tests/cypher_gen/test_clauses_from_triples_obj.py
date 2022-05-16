"""Test cases for Cypher code generation from triples in case relation is to a object"""

from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes import Namespace, Triple

# Generation of where clauses


def test_gen_where_case_obj_var_var_var(cypher_gen: CypherGenerator):
    """No filters when predicate and object are variables"""
    triple = Triple(subject="?s", predicate="?p", object="?o")

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_obj_var_var_lit(cypher_gen: CypherGenerator):
    """No filters when the object is a literal, once the triple is not a edge"""
    triple = Triple(subject="?s", predicate="?p", object="BR")

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_obj_var_var_uri(cypher_gen: CypherGenerator):
    """If the object is a URI, the uri prop of the object shall be used to filter"""
    triple = Triple(subject="?s", predicate="?p", object="place:BR")
    namespaces = [Namespace(abbrev="place", full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == 'WHERE place_BR.uri = "placefullBR" '


def test_gen_where_case_obj_var_uri_var(cypher_gen: CypherGenerator):
    """When predicate is a URI, it shall be used to filter based on type of the edge"""
    triple = Triple(subject="?s", predicate="rdfs:partOf", object="?o")
    namespaces = [Namespace(abbrev="rdfs", full="rdfsfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert (
        where_clause
        == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("rdfsfull") + "partOf" '
    )


def test_gen_where_case_obj_var_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="rdfs:partOf", object="BR")
    namespaces = [Namespace(abbrev="rdfs", full="rdfsfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_obj_var_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate=":partOf", object=":place")
    namespaces = [Namespace(abbrev="", full="rdfsfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert (
        where_clause
        == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("rdfsfull") + "partOf" AND _place.uri = "rdfsfullplace" '
    )


def test_gen_where_case_obj_uri_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="?p", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_obj_uri_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="?p", object="Bla")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_obj_uri_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="?p", object="abbrev:US")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == 'WHERE abbrev_US.uri = "abbrevfullUS" '


def test_gen_where_case_obj_uri_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="abbrev:BLA", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert (
        where_clause
        == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("abbrevfull") + "BLA" '
    )


def test_gen_where_case_obj_uri_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="abbrev:BLA", object="Literal")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert where_clause == ""


def test_gen_where_case_obj_uri_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="abbrev:BLA", object="abbrev:US")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_object_where_clause(triple)

    assert (
        where_clause
        == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("abbrevfull") + "BLA" AND abbrev_US.uri = "abbrevfullUS" '
    )


def test_gen_all_var_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert full_clause == "[(s)-[_relation]-(o) | [s, _relation, o]]"


def test_gen_all_var_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="lit")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert full_clause is None


def test_gen_all_var_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="abbrev:uri")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert (
        full_clause
        == '[(s)-[_relation]-(abbrev_uri) WHERE abbrev_uri.uri = "fulluri" | [s, _relation, abbrev_uri]]'
    )


def test_gen_all_var_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="abbrev:uri", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert (
        full_clause
        == '[(s)-[_relation]-(o) WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("full") + "uri" | [s, _relation, o]]'
    )


def test_gen_all_var_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="abbrev:uri", object="lit")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert full_clause is None


def test_gen_all_var_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="abbrev:uri", object="abbrev:uri")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert (
        full_clause
        == '[(s)-[_relation]-(abbrev_uri) WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("full") + "uri" AND abbrev_uri.uri = "fulluri" | [s, _relation, abbrev_uri]]'
    )


def test_gen_all_uri_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:uri", predicate="?p", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert full_clause == "[(abbrev_uri)-[_relation]-(o) | [abbrev_uri, _relation, o]]"


def test_gen_all_uri_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:uri", predicate="?p", object="lit")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert full_clause is None


def test_gen_all_uri_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:uri", predicate="?p", object="abbrev:uri")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert (
        full_clause
        == '[(abbrev_uri)-[_relation]-(abbrev_uri) WHERE abbrev_uri.uri = "fulluri" | [abbrev_uri, _relation, abbrev_uri]]'
    )


def test_gen_all_uri_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:uri", predicate="abbrev:uri", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert (
        full_clause
        == '[(abbrev_uri)-[_relation]-(o) WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("full") + "uri" | [abbrev_uri, _relation, o]]'
    )


def test_gen_all_uri_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:uri", predicate="abbrev:uri", object="lit")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert full_clause is None


def test_gen_all_uri_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:uri", predicate="abbrev:uri", object="abbrev:uri")
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    cypher_gen.setup_namespaces(namespaces)

    full_clause = cypher_gen.filter_case_object(triple)

    assert (
        full_clause
        == '[(abbrev_uri)-[_relation]-(abbrev_uri) WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("full") + "uri" AND abbrev_uri.uri = "fulluri" | [abbrev_uri, _relation, abbrev_uri]]'
    )
