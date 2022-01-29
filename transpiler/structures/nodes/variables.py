from dataclasses import dataclass
from typing import List, Union, Optional

from .expression import ExpressionNode


@dataclass
class Var:
    name: str

    def __hash__(self):
        return hash(self.name)


@dataclass
class SelectedVar:
    value: Union[str, ExpressionNode]
    alias: Optional[str] = None
