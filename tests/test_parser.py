"""Test parser to construct the query description structure"""
from transpiler.parser import SelectSparqlParser
from transpiler.structures.nodes import *
from transpiler.structures.query import Query


def test_query_basic_1(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o}")

    assert answer == result  # nosec


def test_query_basic_2(switch_parser: SelectSparqlParser):
    """Try to construct a basic query structure with two predicates"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p2", "?o2"), Triple("?s", "?p1", "?o1")]
        ),
        variables=[Var("?s"), Var("?p1"), Var("?o1"), Var("?p2"), Var("?o2")],
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p1 ?o1; ?p2 ?o2 .}")

    assert answer == result  # nosec


def test_query_union_1(switch_parser: SelectSparqlParser):
    """Try to parse a simple query using the UNION keyword"""
    answer = Query(
        mandatory=GraphPattern(
            or_blocks=[
                [
                    GraphPattern(and_triples=[Triple("?s", "?p2", "?o")]),
                    GraphPattern(and_triples=[Triple("?s", "?p1", "?o")]),
                ]
            ]
        ),
        variables=[Var("?s"), Var("?p1"), Var("?o"), Var("?p2")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            { ?s ?p1 ?o }
            UNION
            { ?s ?p2 ?o }
        }"""
    )

    assert result == answer  # nosec


def test_query_union_2(switch_parser: SelectSparqlParser):
    """Try to parse a simple query using the UNION along  with mandatory nodes"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p3", "?o2")],
            or_blocks=[
                [
                    GraphPattern(and_triples=[Triple("?s", "?p2", "?o")]),
                    GraphPattern(and_triples=[Triple("?s", "?p1", "?o")]),
                ]
            ],
        ),
        variables=[
            Var("?s"),
            Var("?p3"),
            Var("?o2"),
            Var("?p1"),
            Var("?o"),
            Var("?p2"),
        ],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p3 ?o2 .
            { ?s ?p1 ?o }
            UNION
            { ?s ?p2 ?o }
        }"""
    )

    assert result == answer  # nosec


def test_query_union_3(switch_parser: SelectSparqlParser):
    """Try to parse a query with nested union structures"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p3", "?o2")],
            or_blocks=[
                [
                    GraphPattern(
                        or_blocks=[
                            [
                                GraphPattern(
                                    and_triples=[Triple("?s1", "?p2", "?o")]
                                ),
                                GraphPattern(
                                    and_triples=[Triple("?s", "?p2", "?o")]
                                ),
                            ]
                        ]
                    ),
                    GraphPattern(and_triples=[Triple("?s", "?p1", "?o")]),
                ]
            ],
        ),
        variables=[
            Var("?s"),
            Var("?p3"),
            Var("?o2"),
            Var("?p1"),
            Var("?o"),
            Var("?p2"),
            Var("?s1"),
        ],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s WHERE {
            ?s ?p3 ?o2 .
            { ?s ?p1 ?o }
            UNION
            {
                { ?s ?p2 ?o }
                UNION
                { ?s1 ?p2 ?o}
            }
        }"""
    )

    assert result == answer  # nosec


def test_query_optional(switch_parser: SelectSparqlParser):
    """Try to parse a simple query with OPTIONAL keyword"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p1", "?o1")],
            optionals=[GraphPattern(and_triples=[Triple("?s", "?p2", "?o2")])],
        ),
        variables=[
            Var("?s"),
            Var("?o1"),
            Var("?p1"),
            Var("?p2"),
            Var("?o2"),
        ],
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(value="?o1"),
            SelectedVar(value="?o2"),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s ?o1 ?o2 WHERE {
            ?s ?p1 ?o1 .
            OPTIONAL {
                ?s ?p2 ?o2
            }
        }"""
    )

    assert result == answer  # nosec


def test_query_minus(switch_parser: SelectSparqlParser):
    """Try to parse a simple query with MINUS keyword"""
    answer = Query(
        mandatory=GraphPattern(
            and_triples=[Triple("?s", "?p1", "?o")],
            minus=[GraphPattern(and_triples=[Triple("?s", "?p2", "?o")])],
        ),
        variables=[
            Var("?s"),
            Var("?o"),
            Var("?p1"),
            Var("?p2"),
        ],
        returning=[SelectedVar(value="?s"), SelectedVar(value="?o")],
    )

    result = switch_parser.parse(
        """
        SELECT ?s ?o WHERE {
            ?s ?p1 ?o .
            MINUS {
                ?s ?p2 ?o
            }
        }"""
    )

    assert result == answer  # nosec


def test_query_prefixed(switch_parser: SelectSparqlParser):
    """Try to parse a simple query using a prefix"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "nmspc:name", "?o")]),
        variables=[
            Var("?s"),
            Var("?o"),
        ],
        namespaces=[Namespace("nmspc:", "<http://name.io#>")],
        returning=[SelectedVar(value="?s")],
    )

    result = switch_parser.parse(
        """
        PREFIX nmspc: <http://name.io#>
        SELECT ?s WHERE {
            ?s nmspc:name  ?o
        }"""
    )

    assert result == answer  # nosec


def test_modifiers_limit(switch_parser: SelectSparqlParser):
    """Test limit modifier identification"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(limit=10),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o} LIMIT 10")

    assert answer == result  # nosec


def test_modifiers_offset(switch_parser: SelectSparqlParser):
    """Test offset modifier identification"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(offset=10),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o} OFFSET 10")

    assert answer == result  # nosec


def test_modifiers_limit_offset(switch_parser: SelectSparqlParser):
    """Test limit followed by offset modifier identification"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(limit=100, offset=10),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse(
        "SELECT * WHERE {?s ?p ?o} OFFSET 10 LIMIT 100"
    )

    assert answer == result  # nosec


def test_modifiers_offset_limit(switch_parser: SelectSparqlParser):
    """Test offset followed by limit modifier identification"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(limit=10, offset=100),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse(
        "SELECT * WHERE {?s ?p ?o} LIMIT 10 OFFSET 100"
    )

    assert answer == result  # nosec


def test_modifiers_order_by_var(switch_parser: SelectSparqlParser):
    """Test order by modifier with a var"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(order=OrderNode([OrderCondition(var="?s")])),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o} ORDER BY ?s")

    assert answer == result  # nosec


def test_modifiers_order_by_vars(switch_parser: SelectSparqlParser):
    """Test order by modifier with multiple vars"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(
            order=OrderNode(
                [
                    OrderCondition(var="?s"),
                    OrderCondition(var="?p"),
                    OrderCondition(var="?o"),
                ]
            )
        ),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o} ORDER BY ?s ?p ?o")

    assert answer == result  # nosec


def test_modifiers_group_by_var(switch_parser: SelectSparqlParser):
    """Test group by modifier with a var"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(
            group=GroupClauseNode([GroupCondition(value="?s")])
        ),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o} GROUP BY ?s")

    assert answer == result  # nosec


def test_modifiers_group_by_multiple_vars(switch_parser: SelectSparqlParser):
    """Test group by modifier with multiple var"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o")],
        modifiers=ModifiersNode(
            group=GroupClauseNode(
                [
                    GroupCondition(value="?s"),
                    GroupCondition(value="?p"),
                    GroupCondition(value="?o"),
                ]
            )
        ),
        returning=[SelectedVar(value="*")],
    )

    result = switch_parser.parse("SELECT * WHERE {?s ?p ?o} GROUP BY ?s ?p ?o")

    assert answer == result  # nosec


def test_modifiers_group_by_with_aggregation(switch_parser: SelectSparqlParser):
    """Test group by modifier with multiple var"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o"), Var("?count")],
        modifiers=ModifiersNode(
            group=GroupClauseNode([GroupCondition(value="?s")])
        ),
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=ExpressionNode(
                    exp=OrExpression(
                        base=AndExpression(
                            base=RelationalExpression(
                                first=AdditiveExpression(
                                    base=MultiplicativeExpression(
                                        base=UnaryExpression(
                                            value=PrimaryExpression(
                                                type=PrimaryType.FUNC,
                                                value=BuiltInFunction(
                                                    name="COUNT", params=["*"]
                                                ),
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?count",
            ),
        ],
    )

    result = switch_parser.parse(
        "SELECT ?s (COUNT(*) AS ?count) WHERE {?s ?p ?o} GROUP BY ?s"
    )

    assert answer == result  # nosec


def test_modifiers_having(switch_parser: SelectSparqlParser):
    """Test having var"""
    answer = Query(
        mandatory=GraphPattern(and_triples=[Triple("?s", "?p", "?o")]),
        variables=[Var("?s"), Var("?p"), Var("?o"), Var("?count")],
        modifiers=ModifiersNode(
            group=GroupClauseNode([GroupCondition(value="?s")]),
            having=HavingClauseNode(
                [
                    ExpressionNode(
                        exp=OrExpression(
                            base=AndExpression(
                                base=RelationalExpression(
                                    first=AdditiveExpression(
                                        base=MultiplicativeExpression(
                                            base=UnaryExpression(
                                                value=PrimaryExpression(
                                                    type=PrimaryType.VAR,
                                                    value="?count",
                                                )
                                            )
                                        )
                                    ),
                                    second=(
                                        LogOperator.GT,
                                        AdditiveExpression(
                                            base=MultiplicativeExpression(
                                                base=UnaryExpression(
                                                    value=PrimaryExpression(
                                                        type=PrimaryType.NUM_LITERAL,
                                                        value=2,
                                                    )
                                                )
                                            )
                                        ),
                                    ),
                                )
                            )
                        )
                    )
                ]
            ),
        ),
        returning=[
            SelectedVar(value="?s"),
            SelectedVar(
                value=ExpressionNode(
                    exp=OrExpression(
                        base=AndExpression(
                            base=RelationalExpression(
                                first=AdditiveExpression(
                                    base=MultiplicativeExpression(
                                        base=UnaryExpression(
                                            value=PrimaryExpression(
                                                type=PrimaryType.FUNC,
                                                value=BuiltInFunction(
                                                    name="COUNT", params=["*"]
                                                ),
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                alias="?count",
            ),
        ],
    )

    result = switch_parser.parse(
        """
        SELECT ?s (COUNT(*) AS ?count) WHERE {
            ?s ?p ?o
        } GROUP BY ?s HAVING(?count > 2)
        """
    )

    assert answer == result  # nosec
