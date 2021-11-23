from dataclasses import dataclass
from typing import Union

from expression import OrExpression


@dataclass
class FilterNode:
    constraint: Union[OrExpression, str]
