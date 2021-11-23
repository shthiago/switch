from dataclasses import dataclass
from typing import List


@dataclass
class Triple:
    subject: str
    predicate: str
    object: str


@dataclass
class GraphPattern:
    and_triples: List[Triple]
    or_block: List[GraphPattern]
