from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
from enum import Enum, auto


class PrimaryType(Enum):
    EXP = auto()
    IRI = auto()
    RDF_LITERAL = auto()
    NUM_LITERAL = auto()
    BOOL_LITERAL = auto()
    VAR = auto()


@dataclass
class BuiltInFunction:
    name: str
    params: List['OrExpression']
    modifiers: Optional[List[str]]


@dataclass
class PrimaryExpression:
    type: PrimaryType
    value: Union[str, int, float, 'OrExpression', BuiltInFunction]


class UnaryOperator(Enum):
    PLUS = auto()
    MINUS = auto()
    NOT = auto()


@dataclass
class UnaryExpression:
    op: UnaryOperator
    value: PrimaryExpression


class MultiplicativeOperator(Enum):
    MULT = auto()
    DIV = auto()


@dataclass
class MultiplicativeExpression:
    base: UnaryExpression
    others: List[Tuple[MultiplicativeOperator, UnaryExpression]]


class AdditiveOperator(Enum):
    SUM = auto()
    SUB = auto()


@dataclass
class AdditiveExpression:
    base: MultiplicativeExpression
    others: List[Tuple[AdditiveOperator, MultiplicativeExpression]]


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
    second: Optional[Tuple[LogOperator, AdditiveExpression]]


@dataclass
class AndExpression:
    base: RelationalExpression
    others: List[RelationalExpression]


@dataclass
class OrExpression:
    base: AndExpression
    others: List[AndExpression]


@dataclass
class ExpressionNode:
    exp: OrExpression
