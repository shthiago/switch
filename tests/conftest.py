from tempfile import NamedTemporaryFile

import pytest
from neo4j import GraphDatabase

from transpiler import lexer, parser, cypher_generator

@pytest.fixture
def switch_lexer() -> lexer.SelectSparqlLexer:
    return lexer.SelectSparqlLexer()


@pytest.fixture
def switch_parser() -> parser.SelectSparqlParser:
    return parser.SelectSparqlParser(debug=True)


@pytest.fixture
def cypher_exec():
    driver = GraphDatabase.driver('neo4j://localhost:7687')
    def _caller(query: str):
        session = driver.session()

        # We don't care about the result, just want to check if the query run
        session.run(query)

    return _caller

@pytest.fixture
def cypher_gen() -> cypher_generator.CypherGenerator:
    return cypher_generator.CypherGenerator()

