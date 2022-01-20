"""Test parser to construct the query description structure"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures import nodes, query


def test_query_basic_1(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s', selected=True),
            nodes.Var('?p', selected=True),
            nodes.Var('?o', selected=True)]
    )

    result = switch_parser.parse('SELECT * WHERE {?s ?p ?o}')

    assert answer == result  # nosec


def test_query_basic_2(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure with two predicates"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p1', '?o1'),
                         nodes.Triple('?s', '?p2', '?o2')]),
        variables=[
            nodes.Var('?s', selected=True),
            nodes.Var('?p1', selected=True),
            nodes.Var('?o1', selected=True),
            nodes.Var('?p2', selected=True),
            nodes.Var('?o2', selected=True)]
    )

    result = switch_parser.parse('SELECT * WHERE {?s ?p1 ?o1; ?p2 ?o2 .}')

    assert answer == result  # nosec


def test_query_union_1(switch_parser: SelectSparqlParser):
    """Try to parse a simple query using the UNION keyword"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            or_block=[
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p1', '?o')]),
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p2', '?o')])]),
        variables=[
            nodes.Var('?s', selected=True),
            nodes.Var('?p1', selected=False),
            nodes.Var('?o', selected=False),
            nodes.Var('?p2', selected=False)]
    )

    result = switch_parser.parse("""
        SELECT ?s WHERE { 
            { ?s ?p1 ?o } 
            UNION 
            { ?s ?p2 ?o }
        }""")

    assert result == answer  # nosec


def test_query_union_2(switch_parser: SelectSparqlParser):
    """Try to parse a simple query using the UNION along  with mandatory nodes"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p3', '?o2')],
            or_block=[
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p1', '?o')]),
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p2', '?o')])]),
        variables=[
            nodes.Var('?s', selected=True),
            nodes.Var('?p1', selected=False),
            nodes.Var('?o', selected=False),
            nodes.Var('?p2', selected=False),
            nodes.Var('?o2', selected=False),
            nodes.Var('?p3', selected=False)]
    )

    result = switch_parser.parse('''
        SELECT ?s WHERE {
            ?s ?p3 ?o2 .
            { ?s ?p1 ?o }
            UNION 
            { ?s ?p2 ?o }
        }''')

    assert result == answer  # nosec


def test_query_union_3(switch_parser: SelectSparqlParser):
    """Try to parse a query with nested union structures"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p3', '?o2')],
            or_block=[
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p1', '?o')]),
                nodes.GraphPattern(
                    or_block=[
                        nodes.GraphPattern(
                            and_triples=[nodes.Triple('?s', '?p2', '?o')]),
                        nodes.GraphPattern(
                            and_triples=[nodes.Triple('?s1', '?p2', '?o')])
                    ])]),
        variables=[
            nodes.Var('?s', selected=True),
            nodes.Var('?p1', selected=False),
            nodes.Var('?o', selected=False),
            nodes.Var('?p2', selected=False),
            nodes.Var('?o2', selected=False),
            nodes.Var('?p3', selected=False),
            nodes.Var('?s1', selected=False)]
    )

    result = switch_parser.parse('''
        SELECT ?s WHERE {
            ?s ?p3 ?o2 .
            { ?s ?p1 ?o }
            UNION 
            { 
                { ?s ?p2 ?o }
                UNION
                { ?s1 ?p2 ?o} 
            }
        }''')

    assert result == answer  # nosec


def test_query_optional(switch_parser: SelectSparqlParser):
    """Try to parse a simple query with OPTIONAL keyword"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p1', '?o1')]),
        optional=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p2', '?o2')]
        ),
        variables=[
            nodes.Var('?s', selected=True),
            nodes.Var('?o1', selected=True),
            nodes.Var('?p1', selected=False),
            nodes.Var('?p2', selected=False),
            nodes.Var('?o2', selected=True),
        ]
    )

    result = switch_parser.parse('''
        SELECT ?s ?o1 ?o2 WHERE {
            ?s ?p1 ?o1 .
            OPTIONAL {
                ?s ?p2 ?o2
            }
        }''')

    assert result == answer  # nosec


def test_query_minus(switch_parser: SelectSparqlParser):
    """Try to parse a simple query with MINUS keyword"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p1', '?o')]),
        minus=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p2', '?o')]
        ),
        variables=[
            nodes.Var('?s', selected=True),
            nodes.Var('?o', selected=True),
            nodes.Var('?p1', selected=False),
            nodes.Var('?p2', selected=False),
        ]
    )

    result = switch_parser.parse('''
        SELECT ?s ?o WHERE {
            ?s ?p1 ?o .
            MINUS {
                ?s ?p2 ?o
            }
        }''')

    assert result == answer  # nosec
