from enum import Enum, auto
from typing import List

from transpiler.structures.nodes.namespace import Namespace

from .parser import SelectSparqlParser

from .structures.query import Query, Triple


class TriplePartType(Enum):
    URI = auto()
    VAR = auto()
    LIT = auto()


class CypherGenerator:
    def __init__(self):
        self.parser = SelectSparqlParser()

    def get_triple_part_type(self, part: str) -> TriplePartType:
        if part[0] == '?':
            return TriplePartType.VAR

        elif ':' in part:
            return TriplePartType.URI

        return TriplePartType.LIT

    def full_uri(self, abbev_uri: str) -> str:
        nms, name = abbev_uri.split(':')
        full_nms = self.namespaces[nms]

        return f'n10s.rdf.shortFormFromFullUri("{full_nms}") + "{name}"'

    def cypher_var_for(self, triple_var: str) -> str:
        return triple_var[1:]

    def case_property_where_clause(self, triple: Triple) -> str:
        pred_type = self.get_triple_part_type(triple.predicate)
        obj_type = self.get_triple_part_type(triple.object)

        filters = []

        if pred_type == TriplePartType.URI:
            filters.append(f'key = {self.full_uri(triple.predicate)}')


        if obj_type == TriplePartType.LIT:
            sub_var = self.cypher_var_for(triple.subject)
            filters.append(f'{sub_var}[key] = "{triple.object}"')

        if not filters:
            return ''

        base = 'WHERE '

        return base + ' AND '.join(filters) + ' '

    def case_property(self, triple: Triple) -> str:
        where_clause = self.case_property_where_clause(triple)

        f'[key in keys(BR) {where_clause}| [BR, key, BR[key]]]'

    def setup_namespaces(self, namespaces: List[Namespace]):
        self.namespaces = {nm.abbrev: nm.full for nm in namespaces}

    def generate(self, sparql_query: str) -> str:
        """Generate cypher from sparql"""
        query = self.parser.parse(sparql_query)

        self.setup_namespaces(query.namespaces)


