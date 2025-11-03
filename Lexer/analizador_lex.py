import ply.lex as lex
from datetime import datetime
import os

# <<< INICIO APORTE Alexandre Icaza

# Palabras reservadas de Swift (keywords y tipos básicos)
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

    # Tipos básicos comunes en declaraciones
    'Int':    'TYPE_INT',
    'Double': 'TYPE_DOUBLE',
    'Bool':   'TYPE_BOOL',
    'String': 'TYPE_STRING',
}

# Lista de tokens
tokens = (
    # Operadores aritméticos
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    
    # Operadores de comparación
    'EQ',  # ==
    'NE',  # !=
    'GT',  # >
    'LT',  # <
    'GE',  # >=
    'LE',  # <=
    
    # Operadores de asignación
    'ASSIGN',        # =
    'PLUS_ASSIGN',   # +=
    'MINUS_ASSIGN',  # -=
    'TIMES_ASSIGN',  # *=
    'DIV_ASSIGN',    # /=
    'MOD_ASSIGN',    # %=

    # Operadores lógicos
    'NOT',  # !
    'AND',  # &&
    'OR',   # ||

    # Operadores ternario y nil-coalescing
    'QUESTION',      # ?
    'COLON',         # :
    'NIL_COALESCE',  # ??

    # Operadores de rango
    'CLOSED_RANGE',     # ...
    'HALF_OPEN_RANGE',  # ..<
    'DOT',              # .

    # Otros tokens necesarios
    'IDENTIFIER',
    'STRING',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',

    'INT_LITERAL',
    'FLOAT_LITERAL',

    'NEWLINE',
) + tuple(reserved.values())


# Estados para comentarios multilínea (/* ... */)
states = (
    ('comment', 'exclusive'),
)

# =========================
# Tokens simples (símbolos)
# =========================

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA  = r','

# Operadores de rango (orden importa: los más largos primero)
t_CLOSED_RANGE    = r'\.\.\.'
t_HALF_OPEN_RANGE = r'\.\.<'
t_DOT             = r'\.'

# Operadores de asignación compuesta
t_PLUS_ASSIGN   = r'\+='
t_MINUS_ASSIGN  = r'-='
t_TIMES_ASSIGN  = r'\*='
t_DIV_ASSIGN    = r'/='
t_MOD_ASSIGN    = r'%='

# Operadores de comparación (los largos primero)
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_LE = r'<='
t_GT = r'>'
t_LT = r'<'

# Operadores lógicos
t_AND = r'&&'
t_OR  = r'\|\|'

# Nil-coalescing
t_NIL_COALESCE = r'\?\?'

# Operadores simples
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_MODULO   = r'%'
t_ASSIGN   = r'='
t_NOT      = r'!'   # también se usa como force unwrap en Swift
t_QUESTION = r'\?'
t_COLON    = r':'


# =========================
# Comentarios
# =========================

# Comentarios de documentación (/// ...) - ignorar
def t_COMMENT_DOC(t):
    r'///.*'
    pass

# Comentarios de línea (// ...) - ignorar
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

# Comentario multilínea: abrimos estado 'comment'
def t_comment(t):
    r'/\*'
    t.lexer.push_state('comment')

# Dentro de 'comment':

def t_comment_comment_end(t):
    r'\*/'
    t.lexer.pop_state()
    pass

def t_comment_comment_content(t):
    r'[^*\n]+'
    pass

def t_comment_comment_star(t):
    r'\*'
    pass

def t_comment_comment_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_comment_error(t):
    # si algo raro aparece dentro del comentario
    t.lexer.skip(1)

# Ignorar espacios dentro del estado comentario
t_comment_ignore = ''


# =========================
# Literales numéricos
# =========================

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    # Ej: 3.14, 0.0, 12.0
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


# =========================
# Strings
# =========================

def t_STRING(t):
    r'"[^"\n]*"'
    # Guardamos sin comillas
    t.value = t.value[1:-1]
    return t


# =========================
# Identificadores y reservadas
# =========================
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # ¿es palabra reservada?
    if t.value in reserved:
        t.type = reserved[t.value]  # ej. 'let' -> 'LET', 'if' -> 'IF'
    return t


# =========================
# Manejo de espacios y saltos de línea
# =========================

# Ignorar espacios y tabs en estado normal
t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


# =========================
# Errores léxicos
# =========================
def t_error(t):
    # reporta y salta el carácter ilegal
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
    t.lexer.skip(1)


# =========================
# Construcción del lexer
# =========================
lexer = lex.lex()


# =========================
# Funciones utilitarias
# =========================

def tokenize_code(code_str: str):
    """
    Toma un string con código Swift y devuelve una lista de tokens:
    {type, value, line, pos}
    """
    lexer.input(code_str)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        result.append({
            "type": tok.type,
            "value": tok.value,
            "line": tok.lineno,
            "pos": tok.lexpos
        })
    return result


def tokenize_and_dump(code_str: str, github_user: str):
    """
    Genera el texto del log:
    - cabecera con usuario y timestamp
    - tabla con línea, pos, tipo de token y valor
    """
    tokens_list = tokenize_code(code_str)

    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")

    log_lines = []
    header = f"LEXICO | usuario={github_user} | fecha-hora={timestamp}"
    log_lines.append("=" * 70)
    log_lines.append(header)
    log_lines.append("=" * 70)
    log_lines.append(f"Total de tokens reconocidos: {len(tokens_list)}\n")
    log_lines.append(f"{'LÍNEA':>6} {'POS':>6}  {'TIPO':>20}  {'VALOR'}")
    log_lines.append("-" * 70)

    for tk in tokens_list:
        valor_str = str(tk['value'])
        if len(valor_str) > 40:
            valor_str = valor_str[:37] + "..."
        log_lines.append(
            f"{tk['line']:>6} {tk['pos']:>6}  {tk['type']:>20}  {valor_str}"
        )

    log_lines.append("=" * 70)
    return "\n".join(log_lines)


def analizar_archivo_swift(ruta_archivo: str, github_user: str):
    """
    Lee un archivo .swift, genera el log y lo guarda en /logs
    con el formato lexico-<user>-<fecha>-<hora>.txt
    """
    print("=" * 70)
    print("ANALIZADOR LÉXICO DE SWIFT - OPERADORES Y COMENTARIOS")
    print("=" * 70)
    print(f"Archivo: {ruta_archivo}")
    print(f"Usuario: {github_user}\n")
    
    # Leer archivo Swift
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo_swift = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        print("Verifica que la ruta sea correcta.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Generar el log en texto
    log_text = tokenize_and_dump(codigo_swift, github_user=github_user)
    
    # Crear carpeta logs/ si no existe
    os.makedirs("logs", exist_ok=True)
    
    # Nombre del archivo de log con timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    filename = f"logs/lexico-{github_user}-{timestamp}.txt"
    
    # Guardar el log a disco
    with open(filename, "w", encoding="utf-8") as f:
        f.write(log_text)
    
    print(f"✅ Log guardado correctamente en: {filename}")
    print(f"   Total de tokens: {len(tokenize_code(codigo_swift))}")


if __name__ == "__main__":
    GITHUB_USER = "todos"
    ARCHIVO_SWIFT = "Examples/pruebaGlobal.swift"

    analizar_archivo_swift(ARCHIVO_SWIFT, GITHUB_USER)

# <<< FIN APORTE Grupal
