"""Main node for the structure"""
from dataclasses import dataclass, field
from typing import Optional, List

from .nodes import *


@dataclass
class Query:
    mandatory: Optional[GraphPattern] = None
    variables: List[Var] = field(default_factory=list)
    modifiers: ModifiersNode = field(default_factory=ModifiersNode)
    namespaces: List[Namespace] = field(default_factory=list)
    returning: List[SelectedVar] = field(default_factory=list)

    def __eq__(self, other):
        if not isinstance(other, Query):
            return False

        return self.mandatory == other.mandatory \
            and set(self.variables) == set(other.variables) \
            and self.modifiers == other.modifiers \
            and set(self.namespaces) == set(other.namespaces) \
            and self.returning == other.returning
