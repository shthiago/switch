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


def test_query_1(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure with two predicates"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple("?s", "?p1", "?o1"),
                         nodes.Triple("?s", "?p2", "?o2")]),
        variables=[
            nodes.Var("?s", selected=True),
            nodes.Var("?p1", selected=True),
            nodes.Var("?o1", selected=True),
            nodes.Var("?p2", selected=True),
            nodes.Var("?o2", selected=True)]
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p1 ?o1; ?p2 ?o2 .}")

    assert answer == result  # nosec
