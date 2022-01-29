"""Check if every sparql function call is being processed"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures import nodes, query


def test_query_rand(switch_parser: SelectSparqlParser):
    """Try to construct a query calling RAND function structure"""
    answer = query.Query(
        mandatory=nodes.GraphPattern(
            and_triples=[nodes.Triple('?s', '?p', '?o')],
            filters=[nodes.FilterNode(
                nodes.ExpressionNode(
                    nodes.OrExpression(
                        nodes.AndExpression(nodes.RelationalExpression(
                            first=nodes.AdditiveExpression(
                                nodes.MultiplicativeExpression(
                                    nodes.UnaryExpression(op=None,
                                                          value=nodes.PrimaryExpression(
                                                              type=nodes.PrimaryType.VAR,
                                                              value='?o')))),
                            second=(nodes.LogOperator.GT,
                                    nodes.AdditiveExpression(
                                        nodes.MultiplicativeExpression(
                                            nodes.UnaryExpression(op=None,
                                                                  value=nodes.BuiltInFunction('RAND', [])))))
                        )))))]),
        variables=[
            nodes.Var('?s'),
            nodes.Var('?p'),
            nodes.Var('?o')
        ],
        returning=[nodes.SelectedVar(value='?s')]
    )

    result = switch_parser.parse("""
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(?o > RAND())
        }
    """)

    assert answer == result  # nosec
