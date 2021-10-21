import pytest

from transpiler import lexer


def test_detect_keyowrds(switch_lexer: lexer.SelectSparqlLexer):
    """Check if lexer recognizes all keywords"""
    for value, token_type in switch_lexer.keywords.items():
        switch_lexer.input(value.lower())
        assert switch_lexer.token().type == token_type
        switch_lexer.input(value.upper())
        assert switch_lexer.token().type == token_type


def test_detect_builtins(switch_lexer: lexer.SelectSparqlLexer):
    """Check if lexer recognizes all built in calls"""
    for value, token_type in switch_lexer.builtin_calls.items():
        switch_lexer.input(value.lower())
        assert switch_lexer.token().type == token_type

        switch_lexer.input(value.upper())
        assert switch_lexer.token().type == token_type


def test_detect_var(switch_lexer: lexer.SelectSparqlLexer):
    """Check if lexer can detect a variable"""
    switch_lexer.input('?var1')
    assert switch_lexer.token().type == 'VAR1'

    switch_lexer.input('$var2')
    assert switch_lexer.token().type == 'VAR2'
