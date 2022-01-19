from dataclasses import dataclass
from typing import List


@dataclass
class Var:
    name: str
    selected: bool = False

    def __hash__(self):
        return hash(self.name)
