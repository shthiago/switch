from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Triple:
    subject: str
    predicate: str
    object: str


@dataclass
class GraphPattern:
    and_triples: Optional[List[Triple]]
    or_block: Optional[List['GraphPattern']]
