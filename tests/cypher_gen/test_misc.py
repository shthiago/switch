from typing import Callable

import pytest

from transpiler.cypher_generator import CypherGenerator, CypherGenerationException
from transpiler.parser import SelectSparqlParser
from transpiler.structures.nodes import Namespace, Triple, namespace


def test_gen_var_for_var(cypher_gen: CypherGenerator):
    assert cypher_gen.cypher_var_for('?var') == 'var'


def test_gen_var_for_uri_0(cypher_gen: CypherGenerator):
    assert cypher_gen.cypher_var_for('p:p') == 'p_p'


def test_gen_var_for_uri_1(cypher_gen: CypherGenerator):
    assert cypher_gen.cypher_var_for(':p') == '_p'


def test_gen_var_for_lit_0(cypher_gen: CypherGenerator):
    with pytest.raises(CypherGenerationException):
        cypher_gen.cypher_var_for('1')


def test_gen_var_for_lit_1(cypher_gen: CypherGenerator):
    with pytest.raises(CypherGenerationException):
        cypher_gen.cypher_var_for(1)
