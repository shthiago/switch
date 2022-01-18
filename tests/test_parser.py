"""Test parser to construct the query description structure"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures import nodes, query


def test_query_1(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple("?s", "?p", "?o")]),
        variables=[
            nodes.Var("?s", selected=True),
            nodes.Var("?p", selected=True),
            nodes.Var("?o", selected=True)]
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o}")

    assert answer == result  # nosec
