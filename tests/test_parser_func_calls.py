"""Check if every sparql function call is being processed"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures.nodes import *
from transpiler.structures.query import Query


def test_query_rand(switch_parser: SelectSparqlParser):
    """Try to construct a query calling RAND function structure"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                op=None,
                                                value=PrimaryExpression(
                                                    type=PrimaryType.VAR,
                                                    value="?o",
                                                ),
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    op=None,
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    ),
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(?o > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_abs(switch_parser: SelectSparqlParser):
    """Test query using the ABS function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "ABS",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(ABS(?o) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_ceil(switch_parser: SelectSparqlParser):
    """Test query using the CEIL function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "CEIL",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(CEIL(?o) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_floor(switch_parser: SelectSparqlParser):
    """Test query using the FLOOR function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "FLOOR",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(FLOOR(?o) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_ceil(switch_parser: SelectSparqlParser):
    """Test query using the CEIL function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "ROUND",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(ROUND(?o) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_concat(switch_parser: SelectSparqlParser):
    """Test query using the CONCAT function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "CONCAT",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?s",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(CONCAT(?o, ?s) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_strlen(switch_parser: SelectSparqlParser):
    """Test query using the STRLEN function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "STRLEN",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(STRLEN(?o) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_ucase(switch_parser: SelectSparqlParser):
    """Test query using the UCASE function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "UCASE",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(UCASE(?o) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_lcase(switch_parser: SelectSparqlParser):
    """Test query using the LCASE function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "LCASE",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            MultiplicativeExpression(
                                                UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.FUNC,
                                                        value=BuiltInFunction(
                                                            "RAND", []
                                                        ),
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(LCASE(?o) > RAND())
        }
    """
    )

    assert answer == result  # nosec


def test_query_contains(switch_parser: SelectSparqlParser):
    """Test query using the CONTAINS function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "CONTAINS",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.STR_LITERAL,
                                                                                            value="abacate",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(CONTAINS(?o, "abacate"))
        }
    """
    )

    assert answer == result  # nosec


def test_query_strstarts(switch_parser: SelectSparqlParser):
    """Test query using the STRSTARTS function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "STRSTARTS",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.STR_LITERAL,
                                                                                            value="ab",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(STRSTARTS(?o, "ab"))
        }
    """
    )

    assert answer == result  # nosec


def test_query_strends(switch_parser: SelectSparqlParser):
    """Test query using the STRENDS function"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
                    ExpressionNode(
                        OrExpression(
                            AndExpression(
                                RelationalExpression(
                                    first=AdditiveExpression(
                                        MultiplicativeExpression(
                                            UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.FUNC,
                                                    value=BuiltInFunction(
                                                        "STRENDS",
                                                        [
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.VAR,
                                                                                            value="?o",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                            ExpressionNode(
                                                                OrExpression(
                                                                    AndExpression(
                                                                        RelationalExpression(
                                                                            first=AdditiveExpression(
                                                                                MultiplicativeExpression(
                                                                                    UnaryExpression(
                                                                                        value=PrimaryExpression(
                                                                                            type=PrimaryType.STR_LITERAL,
                                                                                            value="te",
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            ),
                                                        ],
                                                    ),
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ],
        ),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p ?o .
            FILTER(STRENDS(?o, "te"))
        }
    """
    )

    assert answer == result  # nosec
