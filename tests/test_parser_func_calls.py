"""Check if every sparql function call is being processed"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures.nodes import *
from transpiler.structures.query import Query


def test_query_rand(switch_parser: SelectSparqlParser):
    """Try to construct a query calling RAND function structure"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple('?s', '?p', '?o')],
            filters=[FilterNode(
                ExpressionNode(
                    OrExpression(
                        AndExpression(RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(op=None,
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.VAR,
                                                        value='?o')))),
                            second=(LogOperator.GT,
                                    AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(op=None,
                                                            value=PrimaryExpression(
                                                                type=PrimaryType.FUNC,
                                                                value=BuiltInFunction('RAND', []))))))
                        )))))]),
        variables=[
            Var('?s'),
            Var('?p'),
            Var('?o')
        ],
        returning=[SelectedVar(value='?s')]
    )

    result = switch_parser.parse("""
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(?o > RAND())
        }
    """)

    assert answer == result  # nosec


def test_query_abs(switch_parser: SelectSparqlParser):
    """Test query using the ABS function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple('?s', '?p', '?o')],
            filters=[FilterNode(
                ExpressionNode(
                    OrExpression(
                        AndExpression(RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(value=PrimaryExpression(
                                        type=PrimaryType.FUNC,
                                        value=BuiltInFunction('ABS', [
                                            ExpressionNode(
                                                OrExpression(
                                                    AndExpression(
                                                        RelationalExpression(
                                                            first=AdditiveExpression(
                                                                MultiplicativeExpression(
                                                                    UnaryExpression(value=PrimaryExpression(
                                                                        type=PrimaryType.VAR,
                                                                        value='?o'))))))))]))))),
                            second=(LogOperator.GT,
                                    AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction('RAND', [])))))))))))]),
        variables=[
            Var('?s'),
            Var('?p'),
            Var('?o')
        ],
        returning=[SelectedVar(value='?s')]
    )

    result = switch_parser.parse("""
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(ABS(?o) > RAND())
        }
    """)

    assert answer == result  # nosec
