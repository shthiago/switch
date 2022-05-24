from dataclasses import dataclass
from typing import Optional, Union

from .expression import OrExpression


@dataclass
class Var:
    name: str

    def __hash__(self):
        return hash(self.name)


@dataclass
class SelectedVar:
    value: Union[str, OrExpression]
    alias: Optional[str] = None
