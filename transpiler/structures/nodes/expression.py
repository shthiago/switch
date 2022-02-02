from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Tuple, Union


class PrimaryType(Enum):
    EXP = auto()
    IRI = auto()
    NUM_LITERAL = auto()
    BOOL_LITERAL = auto()
    STR_LITERAL = auto()
    VAR = auto()
    FUNC = auto()


@dataclass
class BuiltInFunction:
    name: str
    params: List["OrExpression"]


@dataclass
class PrimaryExpression:
    type: PrimaryType
    value: Union[str, int, float, "OrExpression", BuiltInFunction]


class UnaryOperator(Enum):
    PLUS = auto()
    MINUS = auto()
    NOT = auto()


@dataclass
class UnaryExpression:
    value: PrimaryExpression
    op: Optional[UnaryOperator] = None


class MultiplicativeOperator(Enum):
    MULT = auto()
    DIV = auto()


@dataclass
class MultiplicativeExpression:
    base: UnaryExpression
    others: List[Tuple[MultiplicativeOperator, UnaryExpression]] = field(
        default_factory=list
    )


class AdditiveOperator(Enum):
    SUM = auto()
    SUB = auto()


@dataclass
class AdditiveExpression:
    base: MultiplicativeExpression
    others: List[Tuple[AdditiveOperator, MultiplicativeExpression]] = field(
        default_factory=list
    )


class LogOperator(Enum):
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    IN = auto()
    NOT_IN = auto()


@dataclass
class RelationalExpression:
    first: AdditiveExpression
    second: Optional[Tuple[LogOperator, AdditiveExpression]] = None


@dataclass
class AndExpression:
    base: RelationalExpression
    others: List[RelationalExpression] = field(default_factory=list)


@dataclass
class OrExpression:
    base: AndExpression
    others: List[AndExpression] = field(default_factory=list)


@dataclass
class ExpressionNode:
    exp: OrExpression
