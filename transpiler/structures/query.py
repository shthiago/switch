"""Main node for the structure"""
from dataclasses import dataclass, field
from typing import Optional


from .nodes import *


@dataclass
class Query:
    filter: Optional[FilterNode] = None
    minus: Optional[MinusNode] = None
    optional: Optional[OptionalNode] = None
    mandatory: Optional[GraphPattern] = None
    variables: List[Var] = field(default_factory=list)
    modifiers: ModifiersNode = field(default_factory=ModifiersNode)
