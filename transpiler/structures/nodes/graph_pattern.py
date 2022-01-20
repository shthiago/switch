from dataclasses import dataclass, field
from typing import List, Optional


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
    or_block: List['GraphPattern'] = field(default_factory=list)

    def __eq__(self, other):
        if not isinstance(other, GraphPattern):
            return False

        return set(self.and_triples) == set(other.and_triples) \
            and set(other.or_block) == set(other.or_block)

    def __hash__(self):
        return hash(str(self))
