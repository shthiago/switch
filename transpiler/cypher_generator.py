from enum import Enum, auto
from typing import Any, List, Optional

from transpiler.structures.nodes.namespace import Namespace

from .parser import SelectSparqlParser
from .structures.query import Triple


class CypherGenerationException(Exception):
    """Failure on a generation process"""


class TriplePartType(Enum):
    URI = auto()
    VAR = auto()
    LIT = auto()


class CypherGenerator:
    def __init__(self):
        self.parser = SelectSparqlParser()

        self.used_variables: List[str] = []

    def get_triple_part_type(self, part: Any) -> TriplePartType:
        if not isinstance(part, str):
            return TriplePartType.LIT

        if part[0] == "?":
            return TriplePartType.VAR

        elif ":" in part:
            return TriplePartType.URI

        return TriplePartType.LIT

    def full_uri(self, abbev_uri: str) -> str:
        nms, name = abbev_uri.split(":")
        full_nms = self.namespaces[nms]

        return f'n10s.rdf.shortFormFromFullUri("{full_nms}") + "{name}"'

    def cypher_var_for(self, triple_part: str) -> str:
        part_type = self.get_triple_part_type(triple_part)
        if part_type == TriplePartType.VAR:
            var = triple_part[1:]

        elif part_type == TriplePartType.URI:
            var = triple_part.replace(':', '_')

        else:
            raise CypherGenerationException(
                f'Cannot generate var for a literal: {triple_part}')

        return var

    def case_property_where_clause(self, triple: Triple) -> str:
        obj_type = self.get_triple_part_type(triple.object)
        if obj_type == TriplePartType.URI:
            return ''

        pred_type = self.get_triple_part_type(triple.predicate)

        filters = []

        if pred_type == TriplePartType.URI:
            filters.append(f"key = {self.full_uri(triple.predicate)}")

        if obj_type == TriplePartType.LIT:
            sub_var = self.cypher_var_for(triple.subject)
            filters.append(f'{sub_var}[key] = "{triple.object}"')

        if not filters:
            return ''

        base = 'WHERE '

        return base + ' AND '.join(filters) + ' '

    def case_object_where_clause(self, triple: Triple) -> str:
        obj_type = self.get_triple_part_type(triple.object)
        if obj_type == TriplePartType.LIT:
            return ''

        pred_type = self.get_triple_part_type(triple.predicate)

        filters = []
        if pred_type == TriplePartType.URI:
            filters.append(
                f'type(_relation) = {self.full_uri(triple.predicate)}')

        if obj_type == TriplePartType.URI:
            obj_var = self.cypher_var_for(triple.object)
            filters.append(f'{obj_var}.uri = {self.full_uri(triple.object)}')

        if not filters:
            return ''

        base = 'WHERE '

        return base + ' AND '.join(filters) + ' '

    def filter_case_property(self, triple: Triple) -> Optional[str]:
        obj_type = self.get_triple_part_type(triple.object)

        if obj_type == TriplePartType.URI:
            return None

        where_clause = self.case_property_where_clause(triple)
        subject = self.cypher_var_for(triple.subject)

        return f'[key in keys({subject}) {where_clause}| [{subject}, key, {subject}[key]]]'

    def filter_case_object(self, triple: Triple) -> Optional[str]:
        object_type = self.get_triple_part_type(triple.object)

        if object_type == TriplePartType.LIT:
            return None

        where_clause = self.case_object_where_clause(triple)
        subject = self.cypher_var_for(triple.subject)
        obj = self.cypher_var_for(triple.object)

        return f'[({subject})-[_relation]-({obj}) {where_clause}| [{subject}, _relation, {obj}]]'

    def with_clause(self, triple: Triple) -> Optional[str]:
        parts = [triple.subject, triple.predicate, triple.object]
        types = list(map(self.get_triple_part_type, parts))

        used: List[str] = []
        with_parts: List[str] = []
        for i, (part, type_) in enumerate(zip(parts, types)):
            if type_ == TriplePartType.VAR:
                varname = self.cypher_var_for(part)
                used.append(varname)
                with_parts.append(f'triples[{i}] AS {varname}')

        for var in reversed(self.used_variables):
            if var not in used:
                with_parts.insert(0, f'{var} AS {var}')

        for used_var in used:
            if used_var not in self.used_variables:
                self.used_variables.append(used_var)

        if not with_parts:
            return None

        return 'WITH ' + ', '.join(with_parts)

    def setup_namespaces(self, namespaces: List[Namespace]):
        self.namespaces = {nm.abbrev: nm.full for nm in namespaces}

    def generate(self, sparql_query: str) -> str:
        """Generate cypher from sparql"""
        query = self.parser.parse(sparql_query)

        self.setup_namespaces(query.namespaces)
