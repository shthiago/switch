from dataclasses import dataclass, field
from typing import List, Optional

from .filter import FilterNode


@dataclass
class Triple:
    subject: str
    predicate: str
    object: str

    def __hash__(self):
        return hash(self.subject + self.predicate + self.object)


@dataclass
class GraphPattern:
    and_triples: List[Triple] = field(default_factory=list)
    or_blocks: List[List["GraphPattern"]] = field(default_factory=list)
    filters: List[FilterNode] = field(default_factory=list)
    minus: List["GraphPattern"] = field(default_factory=list)
    optionals: List["GraphPattern"] = field(default_factory=list)

    def __eq__(self, other):
        if not isinstance(other, GraphPattern):
            return False

        return (
            str(self.and_triples) == str(other.and_triples)
            and str(self.or_blocks) == str(other.or_blocks)
            and str(self.optionals) == str(other.optionals)
            and str(self.minus) == str(other.minus)
            and str(self.filters) == str(other.filters)
        )

    def __hash__(self):
        return hash(str(self))
