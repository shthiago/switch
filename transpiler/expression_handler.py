from typing import Optional

from transpiler.structures.nodes.expression import (
    OrExpression,
    PrimaryExpression,
    PrimaryType,
)


class ExpressionHandler:
    def primary_only(self, node: OrExpression) -> Optional[PrimaryExpression]:
        """Check if a given OrExpression have only a primary"""
        if node.others:
            return None

        and_node = node.base

        if and_node.others:
            return None

        rel_node = and_node.base

        if rel_node.second:
            return None

        add_node = rel_node.first

        if add_node.others:
            return None

        mult_node = add_node.base

        if mult_node.others:
            return None

        unary_node = mult_node.base

        return unary_node.value

    def is_literal(self, node: OrExpression) -> bool:
        primary = self.primary_only(node)

        if primary is None:
            return False

        literal_types = [
            PrimaryType.NUM_LITERAL,
            PrimaryType.STR_LITERAL,
            PrimaryType.BOOL_LITERAL,
        ]

        return primary.type in literal_types

    def is_builtincall(self, node: OrExpression) -> bool:
        primary = self.primary_only(node)

        if primary is None:
            return False

        return primary.type == PrimaryType.FUNC

    def is_iri(self, node: OrExpression) -> bool:
        primary = self.primary_only(node)

        if primary is None:
            return False

        return primary.type == PrimaryType.IRI

    def is_var(self, node: OrExpression) -> bool:
        primary = self.primary_only(node)

        if primary is None:
            return False

        return primary.type == PrimaryType.VAR
