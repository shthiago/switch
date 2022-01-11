"""Modifiers node"""
from dataclasses import dataclass
from typing import Optional, Union, List

from .expression import ExpressionNode, BuiltInFunction
from .variables import Var


@dataclass
class GroupCondition:
    value: Union[Var, ExpressionNode, BuiltInFunction]
    alias: Optional[str] = None


@dataclass
class GroupClauseNode:
    conditions: List[GroupCondition]


@dataclass
class OrderCondition:
    exp: Optional[Union[ExpressionNode,
                        BuiltInFunction]] = None
    var: Optional[str] = None
    order: str = 'DESC'


@dataclass
class OrderNode:
    conditions: List[OrderCondition]


@dataclass
class HavingClauseNode:
    constraints: List[Union[ExpressionNode,
                            BuiltInFunction]]


@dataclass
class ModifiersNode:
    group: Optional[GroupClauseNode] = None
    having: Optional[HavingClauseNode] = None
    order: Optional[OrderNode] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
