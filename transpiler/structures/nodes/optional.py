from dataclasses import dataclass

from graph_pattern import GraphPattern


@dataclass
class OptionalNode:
    graph_pattern: GraphPattern
