from typing import List

from transpiler.structures.nodes.expression import (
    AdditiveExpression,
    AdditiveOperator,
    AndExpression,
    BuiltInFunction,
    LogOperator,
    MultiplicativeExpression,
    MultiplicativeOperator,
    OrExpression,
    PrimaryExpression,
    PrimaryType,
    RelationalExpression,
    UnaryExpression,
    UnaryOperator,
)


class ExpressionHandler:
    def __init__(self):
        self.builtin_gen_map = {
            "COUNT": self._gen_call_for_count,
            "SUM": self._gen_call_for_sum,
            "MIN": self._gen_call_for_min,
            "MAX": self._gen_call_for_max,
            "AVG": self._gen_call_for_avg,
            "STRLEN": self._gen_call_for_strlen,
            "SUBSTR": self._gen_call_for_substr,
            "UCASE": self._gen_call_for_ucase,
            "LCASE": self._gen_call_for_lcase,
            "STRSTARTS": self._gen_call_for_strstarts,
            "STRENDS": self._gen_call_for_strends,
            "CONTAINS": self._gen_call_for_contains,
            "CONCAT": self._gen_call_for_concat,
            "REGEX": self._gen_call_for_regex,
            "REPLACE": self._gen_call_for_replace,
            "COALESCE": self._gen_call_for_coalesce,
            "ABS": self._gen_call_for_abs,
            "ROUND": self._gen_call_for_round,
            "CEIL": self._gen_call_for_ceil,
            "FLOOR": self._gen_call_for_floor,
            "RAND": self._gen_call_for_rand,
            "NOW": self._gen_call_for_now,
            "YEAR": self._gen_call_for_year,
            "MONTH": self._gen_call_for_month,
            "DAY": self._gen_call_for_day,
            "HOURS": self._gen_call_for_hours,
            "MINUTES": self._gen_call_for_minutes,
            "SECONDS": self._gen_call_for_seconds,
            "TIMEZONE": self._gen_call_for_timezone,
            "TZ": self._gen_call_for_tz,
        }

    def value_orexpression(self, node: OrExpression) -> str:
        base_value = self.value_andexpression(node.base)
        if node.others:
            rest = " OR " + " OR ".join(
                [f"({self.value_andexpression(n)})" for n in node.others]
            )
            return f"{base_value}" + rest

        return base_value

    def value_andexpression(self, node: AndExpression) -> str:
        base_value = self.value_relationalexpression(node.base)
        if node.others:
            rest = " AND " + " AND ".join(
                [f"({self.value_relationalexpression(n)})" for n in node.others]
            )
            return f"({base_value})" + rest

        return base_value

    def value_relationalexpression(self, node: RelationalExpression) -> str:
        first = self.value_additiveexpression(node.first)

        if node.second:
            op, value = node.second
            second = self.value_additiveexpression(value)
            fmt_string = self._log_operator_fmt_str(op)

            return f"({fmt_string.format(first, second)})"

        return first

    def value_additiveexpression(self, node: AdditiveExpression) -> str:
        value = self.value_multiplicativeexpression(node.base)
        if not node.others:
            return value

        for op, exp in node.others:
            op_str = self._add_operator_str(op)
            exp_str = self.value_multiplicativeexpression(exp)
            value += f" {op_str} {exp_str}"

        return f"({value})"

    def value_multiplicativeexpression(self, node: MultiplicativeExpression) -> str:
        value = self.value_unaryexpression(node.base)
        if not node.others:
            return value

        for op, exp in node.others:
            op_str = self._mult_operator_str(op)
            exp_str = self.value_unaryexpression(exp)
            value += f" {op_str} {exp_str}"

        return f"({value})"

    def value_unaryexpression(self, node: UnaryExpression) -> str:
        value = self.value_primaryexpression(node.value)
        if not node.op:
            return value

        op = self._unary_operator_str(node.op)

        return f"({op}{value})"

    def value_primaryexpression(self, node: PrimaryExpression) -> str:
        if self.is_literal(node) or self.is_iri(node):
            return node.value

        if self.is_var(node):
            return node.value.replace("?", "")

        if self.is_builtinfunction(node):
            return self.builtinfunction_to_cypher(node.value)

        return self.value_orexpression(node.value)

    def builtinfunction_to_cypher(self, call: BuiltInFunction) -> str:
        return self.builtin_gen_map[call.name](call.params)

    def _gen_call_for_count(self, params: List[OrExpression]):
        arg = self.value_orexpression(params[0])

        return f"count({arg})"

    def _gen_call_for_sum(self, params: List[OrExpression]):
        arg = self.value_orexpression(params[0])

        return f"sum({arg})"

    def _gen_call_for_min(self, params: List[OrExpression]):
        arg = self.value_orexpression(params[0])

        return f"min({arg})"

    def _gen_call_for_max(self, params: List[OrExpression]):
        arg = self.value_orexpression(params[0])

        return f"max({arg})"

    def _gen_call_for_avg(self, params: List[OrExpression]):
        arg = self.value_orexpression(params[0])

        return f"avg({arg})"

    def _gen_call_for_strlen(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_substr(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_ucase(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_lcase(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_strstarts(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_strends(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_contains(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_concat(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_regex(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_replace(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_coalesce(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_abs(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_round(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_ceil(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_floor(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_rand(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_now(self, params: List[OrExpression]):
        return "datetime()"

    def _gen_call_for_year(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_month(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_day(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_hours(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_minutes(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_seconds(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_timezone(self, params: List[OrExpression]):
        raise NotImplementedError

    def _gen_call_for_tz(self, params: List[OrExpression]):
        raise NotImplementedError

    def _unary_operator_str(self, op: UnaryOperator) -> str:
        match op:
            case UnaryOperator.PLUS:
                return "+"
            case UnaryOperator.MINUS:
                return "-"
            case UnaryOperator.NOT:
                return "NOT "

    def _mult_operator_str(self, op: MultiplicativeOperator) -> str:
        match op:
            case MultiplicativeOperator.MULT:
                return "*"
            case MultiplicativeOperator.DIV:
                return "/"

    def _add_operator_str(self, op: AdditiveOperator) -> str:
        match op:
            case AdditiveOperator.SUM:
                return "+"
            case AdditiveOperator.SUB:
                return "-"

    def _log_operator_fmt_str(self, op: LogOperator) -> str:
        match op:
            case LogOperator.EQ:
                return "{} = {}"
            case LogOperator.NEQ:
                return "{} <> {}"
            case LogOperator.LT:
                return "{} < {}"
            case LogOperator.GT:
                return "{} > {}"
            case LogOperator.LTE:
                return "{} <= {}"
            case LogOperator.GTE:
                return "{} >= {}"
            case LogOperator.IN:
                return "{} IN {}"
            case LogOperator.NOT_IN:
                return "NOT {} IN {}"

    def is_literal(self, node: PrimaryExpression) -> bool:
        literal_types = [
            PrimaryType.NUM_LITERAL,
            PrimaryType.STR_LITERAL,
            PrimaryType.BOOL_LITERAL,
        ]

        return node.type in literal_types

    def is_builtinfunction(self, node: PrimaryExpression) -> bool:
        return node.type == PrimaryType.FUNC

    def is_iri(self, node: PrimaryExpression) -> bool:
        return node.type == PrimaryType.IRI

    def is_var(self, node: PrimaryExpression) -> bool:
        return node.type == PrimaryType.VAR
