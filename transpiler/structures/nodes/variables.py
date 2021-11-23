from dataclasses import dataclass
from typing import List


@dataclass
class Var:
    name: str
    selected: bool


@dataclass
class VarsNode:
    variables: List[Var]
