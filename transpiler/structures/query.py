"""Main node for the structure"""
from dataclasses import dataclass
from typing import Optional

from .nodes import *


@dataclass
class Query:
    filter: Optional[FilterNode]
    minus: Optional[MinusNode]
    optional: Optional[OptionalNode]
    mandatory: Optional[GraphPattern]
    variables: Optional[VarsNode]
    modifier: Optional[ModifiersNode]
