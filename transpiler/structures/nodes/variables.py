from dataclasses import dataclass
from typing import Optional, Union

from .expression import OrExpression


@dataclass
class SelectedVar:
    value: Union[str, OrExpression]
    alias: Optional[str] = None
