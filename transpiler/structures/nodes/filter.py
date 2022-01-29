from dataclasses import dataclass
from typing import Union

from .expression import OrExpression, BuiltInFunction


@dataclass
class FilterNode:
    constraint: Union[OrExpression, BuiltInFunction]

    def __hash__(self):
        return hash(str(self))
