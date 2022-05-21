"""Tests for validating behavior of ExpressionNode manipulation"""
import pytest

from transpiler.expression_handler import ExpressionHandler
from transpiler.structures.nodes.expression import (
    AdditiveExpression,
    AdditiveOperator,
    AndExpression,
    BuiltInFunction,
    ExpressionNode,
    LogOperator,
    MultiplicativeExpression,
    MultiplicativeOperator,
    OrExpression,
    PrimaryExpression,
    PrimaryType,
    RelationalExpression,
    UnaryExpression,
)


@pytest.fixture
def handler() -> ExpressionHandler:
    return ExpressionHandler()


def test_gen_count(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.FUNC,
                                value=BuiltInFunction(
                                    name="COUNT",
                                    params=[
                                        OrExpression(
                                            AndExpression(
                                                RelationalExpression(
                                                    first=AdditiveExpression(
                                                        MultiplicativeExpression(
                                                            UnaryExpression(
                                                                value=PrimaryExpression(
                                                                    type=PrimaryType.STR_LITERAL,
                                                                    value="*",
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
    )

    assert handler.value_orexpression(struct) == "count(*)"


def test_gen_sum(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.FUNC,
                                value=BuiltInFunction(
                                    name="SUM",
                                    params=[
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
                                    ],
                                ),
                            )
                        )
                    )
                )
            )
        )
    )

    assert handler.value_orexpression(struct) == "sum(s)"


def test_gen_min(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.FUNC,
                                value=BuiltInFunction(
                                    name="MIN",
                                    params=[
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
                                    ],
                                ),
                            )
                        )
                    )
                )
            )
        )
    )

    assert handler.value_orexpression(struct) == "min(s)"


def test_gen_max(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.FUNC,
                                value=BuiltInFunction(
                                    name="MAX",
                                    params=[
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
                                    ],
                                ),
                            )
                        )
                    )
                )
            )
        )
    )

    assert handler.value_orexpression(struct) == "max(s)"


def test_gen_avg(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.FUNC,
                                value=BuiltInFunction(
                                    name="AVG",
                                    params=[
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
                                    ],
                                ),
                            )
                        )
                    )
                )
            )
        )
    )

    assert handler.value_orexpression(struct) == "avg(s)"
