"""Test cases for Cypher code generation from triples in case relation is to a object"""

from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes import Namespace, Triple


def test_gen_where_case_obj_var_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="?o")

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == ''


def test_gen_where_case_obj_var_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="BR")

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == ''


def test_gen_where_case_obj_var_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="?p", object="place:BR")
    namespaces = [Namespace(abbrev="place",  full="placefull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == 'WHERE place_BR.uri = n10s.rdf.shortFormFromFullUri("placefull") + "BR" '


def test_gen_where_case_obj_var_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="rdfs:partOf", object="?o")
    namespaces = [Namespace(abbrev="rdfs", full="rdfsfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("rdfsfull") + "partOf" '


def test_gen_where_case_obj_var_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate="rdfs:partOf", object="BR")
    namespaces = [Namespace(abbrev="rdfs", full="rdfsfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == ''


def test_gen_where_case_obj_var_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="?s", predicate=":partOf", object=":place")
    namespaces = [Namespace(abbrev="", full="rdfsfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("rdfsfull") + "partOf" AND _place.uri = n10s.rdf.shortFormFromFullUri("rdfsfull") + "place" '


def test_gen_where_case_obj_uri_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="?p", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == ''


def test_gen_where_case_obj_uri_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="?p", object="Bla")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == ''


def test_gen_where_case_obj_uri_var_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="?p", object="abbrev:US")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == 'WHERE abbrev_US.uri = n10s.rdf.shortFormFromFullUri("abbrevfull") + "US" '


def test_gen_where_case_obj_uri_uri_var(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="abbrev:BLA", object="?o")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("abbrevfull") + "BLA" '


def test_gen_where_case_obj_uri_uri_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="abbrev:BLA", object="Literal")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == ''


def test_gen_where_case_obj_uri_uri_uri(cypher_gen: CypherGenerator):
    triple = Triple(subject="abbrev:BR", predicate="abbrev:BLA", object="abbrev:US")
    namespaces = [Namespace(abbrev="abbrev", full="abbrevfull")]
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_node_where_clause(triple)

    assert where_clause == 'WHERE type(_relation) = n10s.rdf.shortFormFromFullUri("abbrevfull") + "BLA" AND abbrev_US.uri = n10s.rdf.shortFormFromFullUri("abbrevfull") + "US" '
