from dataclasses import dataclass


@dataclass
class Namespace:
    abbrev: str
    full: str

    def __hash__(self):
        return hash(self.abbrev + self.full)
