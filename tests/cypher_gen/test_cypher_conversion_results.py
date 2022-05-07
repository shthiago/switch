from typing import Callable

from transpiler.cypher_generator import CypherGenerator
from transpiler.parser import SelectSparqlParser
from transpiler.structures.nodes import Namespace, Triple

# def test_test_fixture(cypher_exec: Callable):
#     cypher_exec('MATCH  (n) RETURN n')

# def test_base_query(cypher_exec: Callable, cypher_generator: CypherGenerator):
#     query = """"
#         SELECT ?s WHERE {
#         ?s ?p ?o
#     }
#     """

#     result = cypher_generator.generate(query)

#     cypher_exec(result)

# def test_base_star_query(cypher_exec: Callable, cypher_generator: CypherGenerator):
#     query = """"
#         SELECT * WHERE {
#         ?s ?p ?o
#     }
#     """

#     result = cypher_generator.generate(query)

#     cypher_exec(result)

# def test_prefixed_query(cypher_exec: Callable, cypher_generator: CypherGenerator):
#     query = """"
#         PREFIX :<http://ontologi.es/place/>
#         PREFIX dct:<http://purl.org/dc/terms/>
#         PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
#         SELECT ?brazilState WHERE {
#             :BR dct:hasPart ?brazilState .
#             ?brazilState rdfs:label ?brazilStateName
#     """

#     result = cypher_generator.generate(query)

#     cypher_exec(result)


def test_gen_case_prop_var_uri_var(
    cypher_gen: CypherGenerator, switch_parser: SelectSparqlParser
):
    namespaces = [Namespace(abbrev="abbrev", full="full")]
    triple = Triple(subject="?s", predicate="abbrev:partOf", object="?o")
    cypher_gen.setup_namespaces(namespaces)

    where_clause = cypher_gen.case_property_where_clause(triple)

    assert (
        where_clause
        == 'WHERE key = n10s.rdf.shortFormFromFullUri("full") + "partOf" '
    )
