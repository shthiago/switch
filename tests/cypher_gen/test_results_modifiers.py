"""Test generation of results modifiers block"""

from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes.modifiers import (
    ModifiersNode,
    OrderCondition,
    OrderNode,
)


def test_gen_none(cypher_gen: CypherGenerator):
    node = ModifiersNode()

    result = cypher_gen.result_modifier(node)

    assert result == ""


def test_gen_order_by_one_var(cypher_gen: CypherGenerator):
    """The order by shall be transformed into the ORDER BY clause"""
    cond = OrderCondition(value="?s")
    node = ModifiersNode(order=OrderNode(conditions=[cond]))

    result = cypher_gen.result_modifier(node)

    assert result == "ORDER BY s ASC"


def test_gen_order_by_two_var(cypher_gen: CypherGenerator):
    """The order by shall be transformed into the ORDER BY clause"""
    cond1 = OrderCondition(value="?s")
    cond2 = OrderCondition(value="?p")
    node = ModifiersNode(order=OrderNode(conditions=[cond1, cond2]))

    result = cypher_gen.result_modifier(node)

    assert result == "ORDER BY s ASC, p ASC"


def test_gen_order_by_two_var_asc(cypher_gen: CypherGenerator):
    """The order by shall be transformed into the ORDER BY clause"""
    cond1 = OrderCondition(value="?s", order="DESC")
    cond2 = OrderCondition(value="?p")
    node = ModifiersNode(order=OrderNode(conditions=[cond1, cond2]))

    result = cypher_gen.result_modifier(node)

    assert result == "ORDER BY s DESC, p ASC"


def test_gen_limit(cypher_gen: CypherGenerator):
    """The limit shall be transformed into LIMIT clause"""
    node = ModifiersNode(limit=5)

    result = cypher_gen.result_modifier(node)

    assert result == "LIMIT 5"


def test_gen_offset(cypher_gen: CypherGenerator):
    """The offset shall be transformed into the SKIP clause"""
    node = ModifiersNode(offset=5)

    result = cypher_gen.result_modifier(node)

    assert result == "SKIP 5"
