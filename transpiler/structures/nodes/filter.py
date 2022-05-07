from dataclasses import dataclass
from typing import Union

from .expression import BuiltInFunction, OrExpression


@dataclass
class FilterNode:
    constraint: Union[OrExpression, BuiltInFunction]

    def __hash__(self):
        return hash(str(self))
