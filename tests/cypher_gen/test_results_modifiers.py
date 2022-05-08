"""Test generation of results modifiers block"""

from transpiler.cypher_generator import CypherGenerator
from transpiler.structures.nodes.modifiers import ModifiersNode, OrderCondition, OrderNode


def test_gen_none(cypher_gen: CypherGenerator):
    node = ModifiersNode()

    result = cypher_gen.result_modifier(node)

    assert result is None

def test_gen_order_by_one_var(cypher_gen: CypherGenerator):
    """The order by shall be transformed into the ORDER BY clause"""
    cond = OrderCondition(var='?s')
    node = ModifiersNode(order=OrderNode(conditions=[cond]))

    result = cypher_gen.result_modifier(node)

    assert result == 'ORDER BY s DESC'


def test_gen_order_by_two_var(cypher_gen: CypherGenerator):
    """The order by shall be transformed into the ORDER BY clause"""
    cond1 = OrderCondition(var='?s')
    cond2 = OrderCondition(var='?p')
    node = ModifiersNode(order=OrderNode(conditions=[cond1, cond2]))

    result = cypher_gen.result_modifier(node)

    assert result == 'ORDER BY s DESC, p DESC'

def test_gen_order_by_two_var_asc(cypher_gen: CypherGenerator):
    """The order by shall be transformed into the ORDER BY clause"""
    cond1 = OrderCondition(var='?s', order='ASC')
    cond2 = OrderCondition(var='?p')
    node = ModifiersNode(order=OrderNode(conditions=[cond1, cond2]))

    result = cypher_gen.result_modifier(node)

    assert result == 'ORDER BY s ASC, p DESC'

def test_gen_limit(cypher_gen: CypherGenerator):
    """The limit shall be transformed into LIMIT clause"""
    node = ModifiersNode(limit=5)

    result = cypher_gen.result_modifier(node)

    assert result == 'LIMIT 5'

def test_gen_offset(cypher_gen: CypherGenerator):
    """The offset shall be transformed into the SKIP clause"""
    node = ModifiersNode(offset=5)

    result = cypher_gen.result_modifier(node)

    assert result == 'SKIP 5'