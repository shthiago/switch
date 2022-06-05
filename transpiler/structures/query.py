"""Main node for the structure"""
from dataclasses import dataclass, field
from typing import List, Optional

from .nodes import GraphPattern, ModifiersNode, Namespace, SelectedVar, Var


@dataclass
class Query:
    graph_pattern: Optional[GraphPattern] = None
    variables: List[Var] = field(default_factory=list)
    modifiers: ModifiersNode = field(default_factory=ModifiersNode)
    namespaces: List[Namespace] = field(default_factory=list)
    returning: List[SelectedVar] = field(default_factory=list)

    def __eq__(self, other):
        if not isinstance(other, Query):
            return False

        return (
            self.graph_pattern == other.graph_pattern
            and set(self.variables) == set(other.variables)
            and self.modifiers == other.modifiers
            and set(self.namespaces) == set(other.namespaces)
            and self.returning == other.returning
        )
