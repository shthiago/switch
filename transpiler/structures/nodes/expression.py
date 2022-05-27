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
    params: List["OrExpression"] = field(default_factory=list)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, BuiltInFunction):
            return False

        return self.name == __o.name and self.params == __o.params


@dataclass
class PrimaryExpression:
    type: PrimaryType
    value: Union[str, int, float, "OrExpression", BuiltInFunction]

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, PrimaryExpression):
            return False

        return self.type == __o.type and self.value == __o.value


class UnaryOperator(Enum):
    PLUS = auto()
    MINUS = auto()
    NOT = auto()


@dataclass
class UnaryExpression:
    value: PrimaryExpression
    op: Optional[UnaryOperator] = None

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, UnaryExpression):
            return False

        return self.value == __o.value and self.op == __o.op


class MultiplicativeOperator(Enum):
    MULT = auto()
    DIV = auto()


@dataclass
class MultiplicativeExpression:
    base: UnaryExpression
    others: List[Tuple[MultiplicativeOperator, UnaryExpression]] = field(
        default_factory=list
    )

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, MultiplicativeExpression):
            return False

        return self.base == __o.base and set(self.others) == set(__o.others)


class AdditiveOperator(Enum):
    SUM = auto()
    SUB = auto()


@dataclass
class AdditiveExpression:
    base: MultiplicativeExpression
    others: List[Tuple[AdditiveOperator, MultiplicativeExpression]] = field(
        default_factory=list
    )

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, AdditiveExpression):
            return False

        return self.base == __o.base and set(self.others) == set(__o.others)


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

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, RelationalExpression):
            return False

        return self.first == __o.first and self.second == __o.second


@dataclass
class AndExpression:
    base: RelationalExpression
    others: List[RelationalExpression] = field(default_factory=list)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, AndExpression):
            return False

        return self.base == __o.base and set(self.others) == set(__o.others)


@dataclass
class OrExpression:
    base: AndExpression
    others: List[AndExpression] = field(default_factory=list)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, OrExpression):
            return False

        return self.base == __o.base and set(self.others) == set(__o.others)
