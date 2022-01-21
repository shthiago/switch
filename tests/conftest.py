import pytest

from transpiler import lexer, parser


@pytest.fixture
def switch_lexer() -> lexer.SelectSparqlLexer:
    return lexer.SelectSparqlLexer()


@pytest.fixture
def switch_parser() -> parser.SelectSparqlParser:
    return parser.SelectSparqlParser(debug=True)
