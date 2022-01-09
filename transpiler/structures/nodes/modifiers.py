"""Modifiers node"""
from dataclasses import dataclass
from typing import Optional

import expression
import graph_pattern

@dataclass
class ModifiersNode:
    group: Optional[expression.ExpressionNode]
    having: Optional[expression.ExpressionNode]
    order_asc: Optional[str]
    order_desc: Optional[str] 
    limit: Optional[int]
    offset: Optional[int]