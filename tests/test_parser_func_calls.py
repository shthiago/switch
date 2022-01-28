"""Check if every sparql function call is being processed"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures import nodes, query


# def test_query_basic_1(switch_parser: SelectSparqlParser):
#     """Try to construct a basic query structure"""
#     answer = query.Query(
#         mandatory=nodes.GraphPattern(
#             and_triples=[nodes.Triple('?s', '?p', '?o')]),
#         variables=[
#             nodes.Var('?s', selected=True),
#             nodes.Var('?p', selected=True),
#             nodes.Var('?o', selected=True)
#         ]
#     )

#     result = switch_parser.parse("""
#         SELECT ?s WHERE {
#             ?s ?p ?o .
#             FILTER(?o > RAND())
#         }
#     """)

# assert answer == result  # nosec
