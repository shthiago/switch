from enum import Enum, auto
from typing import Any, List, Optional

from loguru import logger
from transpiler.structures.nodes import modifiers
from transpiler.structures.nodes.modifiers import ModifiersNode, OrderNode

from transpiler.structures.nodes.namespace import Namespace
from .parser import SelectSparqlParser
from .structures.query import Query, Triple, GraphPattern


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

    def reset_variables(self):
        self.used_variables = []

    def get_triple_part_type(self, part: Any) -> TriplePartType:
        if not isinstance(part, str):
            return TriplePartType.LIT

        if part[0] == "?":
            return TriplePartType.VAR

        elif ":" in part:
            return TriplePartType.URI

        return TriplePartType.LIT

    def ns_uri(self, abbev_uri: str) -> str:
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
            filters.append(f"key = {self.ns_uri(triple.predicate)}")

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
                f'type(_relation) = {self.ns_uri(triple.predicate)}')

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

    def match_clause(self, triple: Triple) -> str:
        subject_type = self.get_triple_part_type(triple.subject)

        if subject_type == TriplePartType.LIT:
            raise CypherGenerationException('Subject cannot be a literal')

        sub_var = self.cypher_var_for(triple.subject)

        if sub_var in self.used_variables:
            return ''

        clause = f'MATCH ({sub_var})'

        if subject_type == TriplePartType.URI:
            clause += f' WHERE {sub_var}.uri = {self.full_uri(triple.subject)}'

        return clause

    def full_uri(self, uri: str) -> str:
        abbrev, name = uri.split(':')
        base = self.namespaces[abbrev]

        return f'"{base + name}"'

    def return_clause(self, query: Query) -> str:
        variables = query.returning
        return_parts = []
        for var in variables:
            if var.alias is None:
                suffix = ''

            else:
                suffix = f' AS {self.cypher_var_for(var.alias)}'

            if isinstance(var.value, str):
                if var.value == '*':
                    varname = '*'
                else:
                    varname = self.cypher_var_for(var.value)

                return_parts.append(f'{varname}{suffix}')

            else:
                raise NotImplementedError

        return 'RETURN ' + ', '.join(return_parts)

    def unwind_clause(self, triple: Triple) -> str:
        cases = [self.filter_case_property(triple),
                 self.filter_case_object(triple)]
        cases = list(filter(lambda k: k is not None, cases))

        return f'UNWIND ' + ' + '.join(cases) + ' AS triples'

    def result_modifier(self, modifiers: ModifiersNode) -> Optional[str]:
        """Given a result modifiers node, generate the code block"""
        if modifiers.group is not None or modifiers.having is not None:
            raise CypherGenerationException(
                'Group By and having not implemented')

        mods = []

        if modifiers.order:
            mods.append(self.order_by_clause(modifiers.order))

        if modifiers.offset:
            mods.append(self.skip_clause(modifiers.offset))

        if modifiers.limit:
            mods.append(self.limit_clause(modifiers.limit))

        if not mods:
            return None

        return '\n'.join(mods)

    def order_by_clause(self, order_node: OrderNode) -> str:
        base = 'ORDER BY '

        cases: List[str] = []

        for cond in order_node.conditions:
            if cond.var is None and cond.exp is not None:
                raise CypherGenerationException(
                    'Order condition by function call not implemented yet')

            cases.append(f'{self.cypher_var_for(cond.var)} {cond.order}')

        return base + ', '.join(cases)

    def skip_clause(self, skip: int) -> str:
        return f'SKIP {skip}'

    def limit_clause(self, limit: int) -> str:
        return f'LIMIT {limit}'

    def parse_query(self, query: str) -> Query:
        return self.parser.parse(query)

    def setup_namespaces(self, namespaces: List[Namespace]):
        self.namespaces = {nm.abbrev: nm.full for nm in namespaces}

    def code_block_for_triple(self, triple: Triple) -> str:
        match_clause = self.match_clause(triple)
        unwind_clause = self.unwind_clause(triple)
        with_clause = self.with_clause(triple)

        return '\n'.join(filter(lambda k: bool(k), [match_clause, unwind_clause, with_clause]))

    def code_block_for_pattern(self, pattern: GraphPattern, query: Query) -> str:
        self.reset_variables()
        codes = []

        if pattern.filters \
                or pattern.minus \
                or pattern.optionals:
            logger.warning(
                'Some features used in the sparql query were not implemented yet.')

        for and_triple in pattern.and_triples:
            codes.append(self.code_block_for_triple(and_triple))

        return '\n'.join(codes) + f'\n{self.return_clause(query)}'

    def split_pattern(self, graph: GraphPattern) -> List[GraphPattern]:
        """Split graph to generate queries

        Given a graph pattern, split it into a list of graph 
        pattern without or_blocks, to concatenate or blocks after
        """
        if graph.or_blocks is None:
            return [graph]

        to_check_blocks = [graph]
        patterns = []
        while to_check_blocks:
            curr_block = to_check_blocks.pop(0)
            if curr_block.or_blocks is not None:
                for lst in curr_block.or_blocks:
                    to_check_blocks.extend(lst)

            patterns.append(curr_block)

        return patterns

    def generate(self, sparql_query: str) -> str:
        """Generate cypher from sparql"""
        query = self.parse_query(sparql_query)
        self.setup_namespaces(query.namespaces)

        patterns = self.split_pattern(query.mandatory)
        # t1 & (t2 or t3)32

        code_blocks = [self.code_block_for_pattern(p, query)
                       for p in patterns
                       if len(p.and_triples) > 0]

        united_code = '\nUNION\n'.join(code_blocks)

        modifiers = self.result_modifier(query.modifiers)

        if modifiers is not None:
            ret_clause = self.return_clause(query)
            modified_code = 'CALL {\n' + united_code + '\n}\n' + ret_clause + '\n' + modifiers

        else:
            modified_code = united_code

        return modified_code


