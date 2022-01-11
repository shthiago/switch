from dataclasses import dataclass

from .graph_pattern import GraphPattern


@dataclass
class MinusNode:
    graph_pattern: GraphPattern
