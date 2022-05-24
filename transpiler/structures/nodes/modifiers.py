"""Modifiers node"""
from dataclasses import dataclass
from typing import List, Optional, Union

from .expression import BuiltInFunction, OrExpression
from .variables import Var


@dataclass
class GroupCondition:
    value: Union[str, OrExpression, BuiltInFunction]
    alias: Optional[str] = None


@dataclass
class GroupClauseNode:
    conditions: List[GroupCondition]


@dataclass
class OrderCondition:
    exp: Optional[Union[OrExpression, BuiltInFunction]] = None
    var: Optional[str] = None
    order: str = "ASC"


@dataclass
class OrderNode:
    conditions: List[OrderCondition]


@dataclass
class HavingClauseNode:
    constraints: List[Union[OrExpression, BuiltInFunction]]


@dataclass
class ModifiersNode:
    group: Optional[GroupClauseNode] = None
    having: Optional[HavingClauseNode] = None
    order: Optional[OrderNode] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
