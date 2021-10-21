import pytest

from transpiler import lexer


@pytest.fixture
def switch_lexer() -> lexer.SelectSparqlLexer:
    return lexer.SelectSparqlLexer()
