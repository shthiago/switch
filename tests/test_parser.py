"""Test parser to construct the query description structure"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures import nodes, query


def test_query_basic_1(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse('SELECT * WHERE {?s ?p ?o}')

    assert answer == result  # nosec


def test_query_basic_2(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure with two predicates"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p2', '?o2'),
                         nodes.Triple('?s', '?p1', '?o1')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p1'),
            nodes.Var('?o1'),
            nodes.Var('?p2'),
            nodes.Var('?o2')],
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse('SELECT * WHERE {?s ?p1 ?o1; ?p2 ?o2 .}')

    assert answer == result  # nosec


def test_query_union_1(switch_parser: SelectSparqlParser):
    """Try to parse a simple query using the UNION keyword"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            or_blocks=[[
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p2', '?o')]),
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p1', '?o')])]]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p1'),
            nodes.Var('?o'),
            nodes.Var('?p2')],
        returning=[nodes.SelectedVar(value='?s')]
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
            or_blocks=[[
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p2', '?o')]),
                nodes.GraphPattern(
                    and_triples=[nodes.Triple('?s', '?p1', '?o')])]]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p3'),
            nodes.Var('?o2'),
            nodes.Var('?p1'),
            nodes.Var('?o'),
            nodes.Var('?p2')],
        returning=[nodes.SelectedVar(value='?s')]
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
            or_blocks=[
                [
                    nodes.GraphPattern(
                        or_blocks=[
                            [
                                nodes.GraphPattern(
                                    and_triples=[nodes.Triple('?s1', '?p2', '?o')]),
                                nodes.GraphPattern(
                                    and_triples=[nodes.Triple('?s', '?p2', '?o')])
                            ]
                        ]
                    ),
                    nodes.GraphPattern(
                        and_triples=[nodes.Triple('?s', '?p1', '?o')])
                ]
            ]
        ),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p3'),
            nodes.Var('?o2'),
            nodes.Var('?p1'),
            nodes.Var('?o'),
            nodes.Var('?p2'),
            nodes.Var('?s1')],
        returning=[nodes.SelectedVar(value='?s')]
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
            and_triples=[nodes.Triple('?s', '?p1', '?o1')],
            optionals=[nodes.GraphPattern(
                and_triples=[nodes.Triple('?s', '?p2', '?o2')]
            )]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?o1'),
            nodes.Var('?p1'),
            nodes.Var('?p2'),
            nodes.Var('?o2'),
        ],
        returning=[nodes.SelectedVar(value='?s'),
                   nodes.SelectedVar(value='?o1'),
                   nodes.SelectedVar(value='?o2')]
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
            and_triples=[nodes.Triple('?s', '?p1', '?o')],
            minus=[nodes.GraphPattern(
                and_triples=[nodes.Triple('?s', '?p2', '?o')]
            )]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?o'),
            nodes.Var('?p1'),
            nodes.Var('?p2'),
        ],
        returning=[nodes.SelectedVar(value='?s'),
                   nodes.SelectedVar(value='?o')]
    )

    result = switch_parser.parse('''
        SELECT ?s ?o WHERE {
            ?s ?p1 ?o .
            MINUS {
                ?s ?p2 ?o
            }
        }''')

    assert result == answer  # nosec


def test_query_prefixed(switch_parser: SelectSparqlParser):
    """Try to parse a simple query using a prefix"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', 'nmspc:name', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?o'),
        ],
        namespaces=[nodes.Namespace('nmspc:', '<http://name.io#>')],
        returning=[nodes.SelectedVar(value='?s')]
    )

    result = switch_parser.parse('''
        PREFIX nmspc: <http://name.io#>
        SELECT ?s WHERE {
            ?s nmspc:name  ?o
        }''')

    assert result == answer  # nosec


def test_modifiers_limit(switch_parser: SelectSparqlParser):
    """Test limit modifier identification"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(limit=10),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse('SELECT * WHERE {?s ?p ?o} LIMIT 10')

    assert answer == result  # nosec


def test_modifiers_offset(switch_parser: SelectSparqlParser):
    """Test offset modifier identification"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(offset=10),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse('SELECT * WHERE {?s ?p ?o} OFFSET 10')

    assert answer == result  # nosec


def test_modifiers_limit_offset(switch_parser: SelectSparqlParser):
    """Test limit followed by offset modifier identification"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(limit=100, offset=10),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse(
        'SELECT * WHERE {?s ?p ?o} OFFSET 10 LIMIT 100')

    assert answer == result  # nosec


def test_modifiers_offset_limit(switch_parser: SelectSparqlParser):
    """Test offset followed by limit modifier identification"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(limit=10, offset=100),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse(
        'SELECT * WHERE {?s ?p ?o} LIMIT 10 OFFSET 100')

    assert answer == result  # nosec


def test_modifiers_order_by_var(switch_parser: SelectSparqlParser):
    """Test order by modifier with a var"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(
            order=nodes.OrderNode([nodes.OrderCondition(var='?s')])),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse(
        'SELECT * WHERE {?s ?p ?o} ORDER BY ?s')

    assert answer == result  # nosec


def test_modifiers_order_by_vars(switch_parser: SelectSparqlParser):
    """Test order by modifier with multiple vars"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(
            order=nodes.OrderNode([nodes.OrderCondition(var='?s'),
                                   nodes.OrderCondition(var='?p'),
                                   nodes.OrderCondition(var='?o')])),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse(
        'SELECT * WHERE {?s ?p ?o} ORDER BY ?s ?p ?o')

    assert answer == result  # nosec


def test_modifiers_group_by_var(switch_parser: SelectSparqlParser):
    """Test group by modifier with a var"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(
            group=nodes.GroupClauseNode([nodes.GroupCondition(value="?s")])),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse(
        'SELECT * WHERE {?s ?p ?o} GROUP BY ?s')

    assert answer == result  # nosec


def test_modifiers_group_by_multiple_vars(switch_parser: SelectSparqlParser):
    """Test group by modifier with multiple var"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')],
        modifiers=nodes.ModifiersNode(
            group=nodes.GroupClauseNode([nodes.GroupCondition(value="?s"),
                                         nodes.GroupCondition(value="?p"),
                                         nodes.GroupCondition(value="?o")])),
        returning=[nodes.SelectedVar(value='*')]
    )

    result = switch_parser.parse(
        'SELECT * WHERE {?s ?p ?o} GROUP BY ?s ?p ?o')

    assert answer == result  # nosec


def test_modifiers_group_by_with_aggregation(switch_parser: SelectSparqlParser):
    """Test group by modifier with multiple var"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o'),
            nodes.Var('?count')],
        modifiers=nodes.ModifiersNode(
            group=nodes.GroupClauseNode([nodes.GroupCondition(value="?s")])),
        returning=[nodes.SelectedVar(value='?s'),
                   nodes.SelectedVar(
                       value=nodes.ExpressionNode(
                           exp=nodes.OrExpression(
                               base=nodes.AndExpression(
                                   base=nodes.RelationalExpression(
                                       first=nodes.AdditiveExpression(
                                           base=nodes.MultiplicativeExpression(
                                               base=nodes.UnaryExpression(value=nodes.BuiltInFunction(
                                                   name='COUNT', params=['*'])))))))),
            alias='?count')]
    )

    result = switch_parser.parse(
        'SELECT ?s (COUNT(*) AS ?count) WHERE {?s ?p ?o} GROUP BY ?s')

    assert answer == result  # nosec


def test_modifiers_having(switch_parser: SelectSparqlParser):
    """Test having var"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o'),
            nodes.Var('?count')],
        modifiers=nodes.ModifiersNode(
            group=nodes.GroupClauseNode([nodes.GroupCondition(value="?s")]),
            having=nodes.HavingClauseNode([
                nodes.ExpressionNode(
                    exp=nodes.OrExpression(
                        base=nodes.AndExpression(
                            base=nodes.RelationalExpression(
                                first=nodes.AdditiveExpression(
                                    base=nodes.MultiplicativeExpression(
                                        base=nodes.UnaryExpression(
                                            value=nodes.PrimaryExpression(
                                                type=nodes.PrimaryType.VAR,
                                                value='?count')))),
                                second=(
                                    nodes.LogOperator.GT,
                                    nodes.AdditiveExpression(
                                        base=nodes.MultiplicativeExpression(
                                            base=nodes.UnaryExpression(
                                                value=nodes.PrimaryExpression(
                                                    type=nodes.PrimaryType.NUM_LITERAL,
                                                    value=2)))))))))])),
        returning=[nodes.SelectedVar(value='?s'),
                   nodes.SelectedVar(
                       value=nodes.ExpressionNode(
                           exp=nodes.OrExpression(
                               base=nodes.AndExpression(
                                   base=nodes.RelationalExpression(
                                       first=nodes.AdditiveExpression(
                                           base=nodes.MultiplicativeExpression(
                                               base=nodes.UnaryExpression(value=nodes.BuiltInFunction(
                                                   name='COUNT', params=['*'])))))))),
            alias='?count')]
    )

    result = switch_parser.parse(
        'SELECT ?s (COUNT(*) AS ?count) WHERE {?s ?p ?o} GROUP BY ?s HAVING(?count > 2)')

    assert answer == result  # nosec
