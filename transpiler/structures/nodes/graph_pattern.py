from dataclasses import dataclass
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
    and_triples: Optional[List[Triple]]
    or_block: Optional[List['GraphPattern']] = None

    def __eq__(self, other):
        if not isinstance(other, GraphPattern):
            return False

        if self.or_block is None and other.or_block is None:
            return set(self.and_triples) == set(other.and_triples)

        elif self.or_block is not None and other.or_block is not None:
            return set(self.and_triples) == set(other.and_triples) \
                and set(other.or_block) == set(other.or_block)

        return False
