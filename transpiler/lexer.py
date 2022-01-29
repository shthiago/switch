from loguru import logger
from ply import lex

from .exceptions import InvalidTokenError


class SelectSparqlLexer:
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self._input = ""

    def input(self, source_code: str, **kwargs):
        self._input = source_code
        self.lexer.input(source_code, **kwargs)

    keywords = {
        "BASE": "KW_BASE",
        "PREFIX": "KW_PREFIX",
        "SELECT": "KW_SELECT",
        "DISTINCT": "KW_DISTINCT",
        "REDUCED": "KW_REDUCED",
        "WHERE": "KW_WHERE",
        "HAVING": "KW_HAVING",
        "ORDER": "KW_ORDER",
        "BY": "KW_BY",
        "ASC": "KW_ASC",
        "DESC": "KW_DESC",
        "LIMIT": "KW_LIMIT",
        "OFFSET": "KW_OFFSET",
        "OPTIONAL": "KW_OPTIONAL",
        "MINUS": "KW_MINUS",
        "UNION": "KW_UNION",
        "FILTER": "KW_FILTER",
        "AS": "KW_AS",
        "NOT": "KW_NOT",
        "IN": "KW_IN",
        "GROUP": "KW_GROUP",
    }

    builtin_calls = {
        "RAND": "FUNC_RAND",
        "ABS": "FUNC_ABS",
        "CEIL": "FUNC_CEIL",
        "FLOOR": "FUNC_FLOOR",
        "ROUND": "FUNC_ROUND",
        "CONCAT": "FUNC_CONCAT",
        "STRLEN": "FUNC_STRLEN",
        "UCASE": "FUNC_UCASE",
        "LCASE": "FUNC_LCASE",
        "CONTAINS": "FUNC_CONTAINS",
        "STRSTARTS": "FUNC_STRSTARTS",
        "STRENDS": "FUNC_STRENDS",
        "YEAR": "FUNC_YEAR",
        "MONTH": "FUNC_MONTH",
        "DAY": "FUNC_DAY",
        "HOURS": "FUNC_HOURS",
        "MINUTES": "FUNC_MINUTES",
        "SECONDS": "FUNC_SECONDS",
        "TIMEZONE": "FUNC_TIMEZONE",
        "TZ": "FUNC_TZ",
        "NOW": "FUNC_NOW",
        "COALESCE": "FUNC_COALESCE",
        "REGEX": "FUNC_REGEX",
        "COUNT": "FUNC_COUNT",
        "SUM": "FUNC_SUM",
        "MIN": "FUNC_MIN",
        "MAX": "FUNC_MAX",
        "AVG": "FUNC_AVG",
        "SUBSTR": "FUNC_SUBSTR",
        "REPLACE": "FUNC_REPLACE",
    }

    tokens = [
        # Keywords
        *keywords.values(),
        # Builtin calls
        *builtin_calls.values(),
        # Terminals
        "ANON",
        "BLANK_NODE_LABEL",
        "DECIMAL",
        "DECIMAL_NEGATIVE",
        "DECIMAL_POSITIVE",
        "DOUBLE",
        "DOUBLE_NEGATIVE",
        "DOUBLE_POSITIVE",
        "INTEGER",
        "INTEGER_NEGATIVE",
        "INTEGER_POSITIVE",
        "IRIREF",
        "LANGTAG",
        "NIL",
        "PNAME_LN",
        "PNAME_NS",
        "STRING_LITERAL1",
        "STRING_LITERAL2",
        "STRING_LITERAL_LONG1",
        "STRING_LITERAL_LONG2",
        "VAR1",
        "VAR2",
        # Symbols
        "SYMB_ASTERISK",
        "SYMB_LP",
        "SYMB_RP",
        "SYMB_LCB",
        "SYMB_RCB",
        "SYMB_LSB",
        "SYMB_RSB",
        "SYMB_DOT",
        "SYMB_COMMA",
        "SYMB_SEMICOLON",
        "SYMB_a",
        "SYMB_PIPE",
        "SYMB_SLASH",
        "SYMB_CIRCUMFLEX",
        "SYMB_QUESTION",
        "SYMB_EXCLAMATION",
        "SYMB_PLUS",
        "SYMB_MINUS",
        "SYMB_OR",
        "SYMB_AND",
        "SYMB_C2",
        "SYMB_EQ",
        "SYMB_NEQ",
        "SYMB_GT",
        "SYMB_LT",
        "SYMB_GTE",
        "SYMB_LTE",
        "SYMB_TRUE",
        "SYMB_FALSE",
    ]

    # Shared constructions
    HEX = r"[0-9A-Fa-f]"
    WS = r" "
    ECHAR = r"\\[tbnrf\"\']"
    PN_LOCAL_ESC = r"\\[_~\.\-!$&\'\(\)\*\+,;=/\?#@%]"
    PERCENT = "%" + HEX + HEX
    PLX = PERCENT + r"|" + PN_LOCAL_ESC
    PN_CHARS_BASE = r"[A-Za-z]"
    PN_CHARS_U = PN_CHARS_BASE + r"|_"
    PN_CHARS = PN_CHARS_U + r"|\-|[0-9]"
    PN_PREFIX = PN_CHARS_BASE + r"(((" + PN_CHARS + r")|\.)*" + PN_CHARS + r")?"
    EXPONENT = r"[eE][+-]?[0-9]+"
    VARNAME = r"(" + PN_CHARS_U + r"|[0-9])+"

    PN_LOCAL = (
        r"("
        + PN_CHARS_U
        + r"|:|[0-9]|"
        + PLX
        + r")(("
        + PN_CHARS
        + r"|\.|:|"
        + PLX
        + ")*("
        + PN_CHARS
        + "|:|"
        + PLX
        + r"))?"
    )

    # Regexes

    t_IRIREF = r'<([^<>"{}|^`\\ ])*>'
    t_INTEGER = r"[0-9]+"
    t_LANGTAG = r"@[a-zA-Z]+(-[a-zA-Z0-9]+)*"
    t_DECIMAL = r"[0-9]*\.[0-9]+"
    t_INTEGER_POSITIVE = r"\+" + t_INTEGER
    t_INTEGER_NEGATIVE = r"-" + t_INTEGER
    t_DECIMAL_POSITIVE = r"\+" + t_DECIMAL
    t_DECIMAL_NEGATIVE = r"\-" + t_DECIMAL
    t_DOUBLE = (
        r"([0-9]+\.[0-9]*"
        + EXPONENT
        + ")"
        + r"|(\.[0-9]+"
        + EXPONENT
        + ")"
        + r"|([0-9]+"
        + EXPONENT
        + ")"
    )
    t_DOUBLE_POSITIVE = r"\+(" + t_DOUBLE + ")"
    t_DOUBLE_NEGATIVE = r"\-(" + t_DOUBLE + ")"
    t_VAR1 = r"\?" + VARNAME
    t_VAR2 = r"\$" + VARNAME
    t_NIL = r"\(\)"
    t_ANON = r"\[\]"
    t_STRING_LITERAL1 = r"\'.*\'"
    t_STRING_LITERAL2 = r'".*"'
    t_PNAME_NS = PN_PREFIX + r":"
    t_PNAME_LN = t_PNAME_NS + PN_LOCAL
    t_BLANK_NODE_LABEL = (
        r"_:(("
        + PN_CHARS_U
        + r")|[0-9])((("
        + PN_CHARS
        + r")|.)("
        + PN_CHARS
        + r"))?"
    )
    t_STRING_LITERAL_LONG1 = r"'''(.|\n)*'''"
    t_STRING_LITERAL_LONG2 = r'"""(.|\n)*"""'

    t_KW_BASE = r"BASE"
    t_KW_PREFIX = r"PREFIX"
    t_KW_SELECT = r"SELECT"
    t_KW_DISTINCT = r"DISTINCT"
    t_KW_REDUCED = r"REDUCED"
    t_KW_WHERE = r"WHERE"
    t_KW_HAVING = r"HAVING"
    t_KW_ORDER = r"ORDER"
    t_KW_BY = r"BY"
    t_KW_ASC = r"ASC"
    t_KW_DESC = r"DESC"
    t_KW_LIMIT = r"LIMIT"
    t_KW_OFFSET = r"OFFSET"
    t_KW_OPTIONAL = r"OPTIONAL"
    t_KW_MINUS = r"MINUS"
    t_KW_UNION = r"UNION"
    t_KW_FILTER = r"FILTER"
    t_KW_AS = r"AS"
    t_KW_NOT = r"NOT"
    t_KW_IN = r"IN"
    t_KW_GROUP = r"GROUP"
    t_FUNC_RAND = r"RAND"
    t_FUNC_ABS = r"ABS"
    t_FUNC_CEIL = r"CEIL"
    t_FUNC_FLOOR = r"FLOOR"
    t_FUNC_ROUND = r"ROUND"
    t_FUNC_CONCAT = r"CONCAT"
    t_FUNC_STRLEN = r"STRLEN"
    t_FUNC_UCASE = r"UCASE"
    t_FUNC_LCASE = r"LCASE"
    t_FUNC_CONTAINS = r"CONTAINS"
    t_FUNC_STRSTARTS = r"STRSTARTS"
    t_FUNC_STRENDS = r"STRENDS"
    t_FUNC_YEAR = r"YEAR"
    t_FUNC_MONTH = r"MONTH"
    t_FUNC_DAY = r"DAY"
    t_FUNC_HOURS = r"HOURS"
    t_FUNC_MINUTES = r"MINUTES"
    t_FUNC_SECONDS = r"SECONDS"
    t_FUNC_TIMEZONE = r"TIMEZONE"
    t_FUNC_TZ = r"TZ"
    t_FUNC_NOW = r"NOW"
    t_FUNC_COALESCE = r"COALESCE"
    t_FUNC_REGEX = r"REGEX"
    t_FUNC_COUNT = r"COUNT"
    t_FUNC_SUM = r"SUM"
    t_FUNC_MIN = r"MIN"
    t_FUNC_MAX = r"MAX"
    t_FUNC_AVG = r"AVG"
    t_FUNC_SUBSTR = r"SUBSTR"
    t_FUNC_REPLACE = r"REPLACE"
    t_SYMB_ASTERISK = r"\*"
    t_SYMB_LP = r"\("
    t_SYMB_RP = r"\)"
    t_SYMB_LCB = r"{"
    t_SYMB_RCB = r"}"
    t_SYMB_LSB = r"\["
    t_SYMB_RSB = r"\]"
    t_SYMB_DOT = r"\."
    t_SYMB_COMMA = r","
    t_SYMB_SEMICOLON = r";"
    t_SYMB_a = r"a"
    t_SYMB_PIPE = r"\|"
    t_SYMB_SLASH = r"/"
    t_SYMB_CIRCUMFLEX = r"\^"
    t_SYMB_QUESTION = r"\?"
    t_SYMB_EXCLAMATION = r"\!"
    t_SYMB_PLUS = r"\+"
    t_SYMB_MINUS = r"\-"
    t_SYMB_OR = r"\|\|"
    t_SYMB_AND = r"&&"
    t_SYMB_C2 = r"\^\^"
    t_SYMB_EQ = r"="
    t_SYMB_NEQ = r"!="
    t_SYMB_GT = r">"
    t_SYMB_LT = r"<"
    t_SYMB_GTE = r">="
    t_SYMB_LTE = r"<="
    t_SYMB_TRUE = r"true"
    t_SYMB_FALSE = r"false"

    t_ignore = " "

    def t_newline(self, token: lex.Token):
        r"\n+"
        token.lexer.lineno += token.value.count("\n")

    def token(self) -> lex.Token:
        return self.lexer.token()

    def t_error(self, token: lex.Token):
        raise InvalidTokenError(
            "Illegal character '%s' at line %s, column %s"
            % (token.value[0], token.lexer.lineno, self.find_column(token))
        )

    def find_column(self, token: lex.Token):
        line_start = self._input.rfind("\n", 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
