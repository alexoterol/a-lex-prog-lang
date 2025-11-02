import ply.lex as lex

reserved = {
    'let': 'LET',
    'var': 'VAR',
    'nil': 'NIL',
    'true': 'TRUE',
    'false': 'FALSE',
    'self': 'SELF',

    'if': 'IF',
    'else': 'ELSE',
    'guard': 'GUARD',
    'for': 'FOR',
    'in': 'IN',
    'while': 'WHILE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'return': 'RETURN',

    'struct': 'STRUCT',
    'class': 'CLASS',
    'enum': 'ENUM',
    'protocol': 'PROTOCOL',
    'extension': 'EXTENSION',

    'func': 'FUNC',
    'init': 'INIT',
    'get': 'GET',
    'set': 'SET',
    'didSet': 'DIDSET',
    'willSet': 'WILLSET',
    'static': 'STATIC',

    'do': 'DO',
    'try': 'TRY',
    'catch': 'CATCH',
    'throw': 'THROW',
    'throws': 'THROWS',
    'async': 'ASYNC',
    'await': 'AWAIT',
    'defer': 'DEFER',
    'some': 'SOME',

    'import': 'IMPORT',
    'private': 'PRIVATE',
    'internal': 'INTERNAL',
    'public': 'PUBLIC',
}

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'STRING',

    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'COLON',

    'CLOSED_RANGE',
    'HALF_OPEN_RANGE',
    'DOT',

] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_COLON = r':'

t_CLOSED_RANGE = r'\.\.\.'
t_HALF_OPEN_RANGE = r'\.\.<'
t_DOT = r'\.'

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
    t.lexer.skip(1)

