"""Check if every sparql function call is being processed"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures.nodes import (
    AdditiveExpression,
    AndExpression,
    BuiltInFunction,
    FilterNode,
    GraphPattern,
    LogOperator,
    MultiplicativeExpression,
    OrExpression,
    PrimaryExpression,
    PrimaryType,
    RelationalExpression,
    SelectedVar,
    Triple,
    UnaryExpression,
    Var,
)
from transpiler.structures.query import Query


def test_query_rand(switch_parser: SelectSparqlParser):
    """Try to construct a query calling RAND function structure"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                ),
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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


def test_query_round(switch_parser: SelectSparqlParser):
    """Test query using the CEIL function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                        ),
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                    value=BuiltInFunction("RAND", []),
                                                )
                                            )
                                        )
                                    ),
                                ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                        ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                        ),
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
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
            filters=[
                FilterNode(
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
                                                        ),
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


def test_query_now(switch_parser: SelectSparqlParser):
    """Test query using the NOW function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?now"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction("NOW"),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?now",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (NOW() AS ?now) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec


def test_query_year(switch_parser: SelectSparqlParser):
    """Test query using the YEAR function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?year"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction(
                                                "YEAR",
                                                [
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
                                                ],
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?year",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (YEAR(?o) AS ?year) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec


def test_query_month(switch_parser: SelectSparqlParser):
    """Test query using the MONTH function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?month"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction(
                                                "MONTH",
                                                [
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
                                                ],
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?month",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (MONTH(?o) AS ?month) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec


def test_query_minutes(switch_parser: SelectSparqlParser):
    """Test query using the MINUTES function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?minute"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction(
                                                "MINUTES",
                                                [
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
                                                ],
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?minute",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (MINUTES(?o) AS ?minute) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec


def test_query_seconds(switch_parser: SelectSparqlParser):
    """Test query using the SECONDS function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?seconds"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction(
                                                "SECONDS",
                                                [
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
                                                ],
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?seconds",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (SECONDS(?o) AS ?seconds) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec


def test_query_timezone(switch_parser: SelectSparqlParser):
    """Test query using the TIMEZONE function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?tz"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction(
                                                "TIMEZONE",
                                                [
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
                                                ],
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?tz",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (TIMEZONE(?o) AS ?tz) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec


def test_query_tz(switch_parser: SelectSparqlParser):
    """Test query using the TZ function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?tz"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction(
                                                "TZ",
                                                [
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
                                                ],
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?tz",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (TZ(?o) AS ?tz) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec


def test_query_coalesce(switch_parser: SelectSparqlParser):
    """Test query using the COALESCE function"""
    answer = Query(
        graph_pattern=GraphPattern(
            and_triples=[Triple("?s", "?p", "?o")],
        ),
        variables=[Var("?s"), Var("?tz"), Var("?p"), Var("?o")],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=OrExpression(
                    AndExpression(
                        RelationalExpression(
                            first=AdditiveExpression(
                                MultiplicativeExpression(
                                    UnaryExpression(
                                        value=PrimaryExpression(
                                            type=PrimaryType.FUNC,
                                            value=BuiltInFunction(
                                                "COALESCE",
                                                [
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
                                                    ),
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
                                                    ),
                                                ],
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?tz",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (COALESCE(?o, "abacate") AS ?tz) WHERE {
            ?s ?p ?o
        }
    """
    )

    assert answer == result  # nosec
