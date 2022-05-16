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


def test_detect_only_var(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.VAR,
                                value="?o",
                            ),
                        )
                    )
                )
            )
        )
    )

    assert handler.is_var(struct)


def test_detect_not_only_var_0(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.STR_LITERAL,
                                value="o",
                            ),
                        )
                    )
                )
            )
        )
    )

    assert not handler.is_var(struct)


def test_detect_not_only_var_1(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.VAR,
                                value="?o",
                            ),
                        )
                    )
                ),
                second=(
                    LogOperator.EQ,
                    AdditiveExpression(
                        MultiplicativeExpression(
                            UnaryExpression(PrimaryExpression(PrimaryType.VAR, "?s"))
                        )
                    ),
                ),
            )
        )
    )

    assert not handler.is_var(struct)


def test_detect_not_only_var_2(handler: ExpressionHandler):
    struct = OrExpression(
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
                    ),
                    others=[
                        (
                            AdditiveOperator.SUM,
                            MultiplicativeExpression(
                                UnaryExpression(
                                    PrimaryExpression(PrimaryType.NUM_LITERAL, 10)
                                )
                            ),
                        )
                    ],
                )
            )
        )
    )

    assert not handler.is_var(struct)


def test_detect_not_only_var_3(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.VAR,
                                value="?o",
                            )
                        ),
                        [
                            (
                                MultiplicativeOperator.MULT,
                                UnaryExpression(
                                    PrimaryExpression(PrimaryType.NUM_LITERAL, 10)
                                ),
                            )
                        ],
                    )
                )
            )
        )
    )

    assert not handler.is_var(struct)


def test_detect_not_only_var_4(handler: ExpressionHandler):
    struct = OrExpression(
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
            ),
            [
                RelationalExpression(
                    AdditiveExpression(
                        MultiplicativeExpression(
                            UnaryExpression(PrimaryExpression(PrimaryType.VAR, "?s"))
                        )
                    )
                )
            ],
        )
    )

    assert not handler.is_var(struct)


def test_detect_not_only_var_5(handler: ExpressionHandler):
    struct = OrExpression(
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
            ),
        ),
        [
            AndExpression(
                RelationalExpression(
                    AdditiveExpression(
                        MultiplicativeExpression(
                            UnaryExpression(PrimaryExpression(PrimaryType.VAR, "?s"))
                        )
                    )
                )
            )
        ],
    )

    assert not handler.is_var(struct)


def test_detect_only_iri(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.IRI,
                                value="abbrev:thing",
                            ),
                        )
                    )
                )
            )
        )
    )

    assert handler.is_iri(struct)


def test_detect_not_only_iri_0(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.STR_LITERAL,
                                value="o",
                            ),
                        )
                    )
                )
            )
        )
    )

    assert not handler.is_iri(struct)


def test_detect_not_only_iri_1(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.IRI,
                                value="abbrev:thing",
                            ),
                        )
                    )
                ),
                second=(
                    LogOperator.EQ,
                    AdditiveExpression(
                        MultiplicativeExpression(
                            UnaryExpression(PrimaryExpression(PrimaryType.VAR, "?s"))
                        )
                    ),
                ),
            )
        )
    )

    assert not handler.is_iri(struct)


def test_detect_not_only_iri_2(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.IRI,
                                value="abbrev:thing",
                            )
                        )
                    ),
                    others=[
                        (
                            AdditiveOperator.SUM,
                            MultiplicativeExpression(
                                UnaryExpression(
                                    PrimaryExpression(PrimaryType.NUM_LITERAL, 10)
                                )
                            ),
                        )
                    ],
                )
            )
        )
    )

    assert not handler.is_iri(struct)


def test_detect_not_only_iri_3(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.IRI,
                                value="abbrev:thing",
                            )
                        ),
                        [
                            (
                                MultiplicativeOperator.MULT,
                                UnaryExpression(
                                    PrimaryExpression(PrimaryType.NUM_LITERAL, 10)
                                ),
                            )
                        ],
                    )
                )
            )
        )
    )

    assert not handler.is_iri(struct)


def test_detect_not_only_iri_4(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.IRI,
                                value="abbrev:thing",
                            )
                        )
                    )
                )
            ),
            [
                RelationalExpression(
                    AdditiveExpression(
                        MultiplicativeExpression(
                            UnaryExpression(PrimaryExpression(PrimaryType.VAR, "?s"))
                        )
                    )
                )
            ],
        )
    )

    assert not handler.is_iri(struct)


def test_detect_not_only_iri_5(handler: ExpressionHandler):
    struct = OrExpression(
        AndExpression(
            RelationalExpression(
                first=AdditiveExpression(
                    MultiplicativeExpression(
                        UnaryExpression(
                            value=PrimaryExpression(
                                type=PrimaryType.IRI,
                                value="abbrev:thing",
                            )
                        )
                    )
                )
            ),
        ),
        [
            AndExpression(
                RelationalExpression(
                    AdditiveExpression(
                        MultiplicativeExpression(
                            UnaryExpression(PrimaryExpression(PrimaryType.VAR, "?s"))
                        )
                    )
                )
            )
        ],
    )

    assert not handler.is_iri(struct)
