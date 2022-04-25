from typing import Callable

from transpiler.structures.nodes import  Triple, Namespace
from transpiler.parser import SelectSparqlParser
from transpiler.cypher_generator import CypherGenerator


def test_gen_case_prop_var_uri_var(cypher_gen: CypherGenerator):
    namespaces = [Namespace(abbrev='abbrev', full='full')]
    triple = Triple(subject='?s', predicate='abbrev:partOf', object='?o')
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)
    
    assert where_clause == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "partOf" '


def test_gen_case_prop_var_var_var(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='?p', object='?o')
    where_clause = cypher_gen.case_property_where_clause(triple)
    
    assert where_clause == ''


def test_gen_case_prop_var_uri_lit(cypher_gen: CypherGenerator):
    namespaces = [Namespace(abbrev='abbrev', full='full')]
    triple = Triple(subject='?s', predicate='abbrev:partOf', object='BR')
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)
    
    assert where_clause == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "partOf" AND s[key] = "BR" '


def test_gen_case_prop_var_var_lit(cypher_gen: CypherGenerator):
    triple = Triple(subject='?s', predicate='?p', object='BR')

    where_clause = cypher_gen.case_property_where_clause(triple)
    
    assert where_clause == 'WHERE s[key] = "BR" '