from typing import Optional, Union

from transpiler.structures.nodes.expression import (
    AdditiveExpression,
    AndExpression,
    MultiplicativeExpression,
    OrExpression,
    PrimaryExpression,
    PrimaryType,
    RelationalExpression,
    UnaryExpression,
)


class ExpressionHandler:
    def primary_only(
        self,
        node: Union[
            OrExpression,
            AndExpression,
            RelationalExpression,
            AdditiveExpression,
            MultiplicativeExpression,
            UnaryExpression,
        ],
    ) -> Optional[PrimaryExpression]:
        """Check if a given expression have only a primary"""
        node_type = type(node).__name__
        match node_type:
            case "OrExpression":
                return self._primary_only_orexpression(node)
            case "AndExpression":
                return self._primary_only_andexpression(node)
            case "RelationalExpression":
                return self._primary_only_relationalexpression(node)
            case "AdditiveExpression":
                return self._primary_only_additiveexpression(node)
            case "MultiplicativeExpression":
                return self._primary_only_multiplicativeexpression(node)
            case "UnaryExpression":
                return self._primary_only_unaryexpression(node)
            case _:
                raise Exception(f"Unexpected type: {node_type}")

    def _primary_only_unaryexpression(
        self, node: UnaryExpression
    ) -> Optional[PrimaryExpression]:
        if node.op:
            return None

        return node.value

    def _primary_only_multiplicativeexpression(
        self, node: MultiplicativeExpression
    ) -> Optional[PrimaryExpression]:
        if node.others:
            return None

        return self._primary_only_unaryexpression(node.base)

    def _primary_only_additiveexpression(
        self, node: AndExpression
    ) -> Optional[PrimaryExpression]:
        if node.others:
            return None

        return self._primary_only_multiplicativeexpression(node.base)

    def _primary_only_relationalexpression(
        self, node: RelationalExpression
    ) -> Optional[PrimaryExpression]:
        if node.second:
            return None

        return self._primary_only_additiveexpression(node.first)

    def _primary_only_andexpression(
        self, node: AndExpression
    ) -> Optional[PrimaryExpression]:
        if node.others:
            return None

        return self._primary_only_relationalexpression(node.base)

    def _primary_only_orexpression(
        self, node: OrExpression
    ) -> Optional[PrimaryExpression]:
        if node.others:
            return None

        return self._primary_only_andexpression(node.base)

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
