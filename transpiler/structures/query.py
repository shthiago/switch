"""Main node for the structure"""
from dataclasses import dataclass
from typing import Optional

from .nodes import *


@dataclass
class Query:
    filter: Optional[FilterNode] = None
    minus: Optional[MinusNode] = None
    optional: Optional[OptionalNode] = None
    mandatory: Optional[GraphPattern] = None
    variables: VarsNode = VarsNode([])
    modifiers: ModifiersNode = ModifiersNode()
