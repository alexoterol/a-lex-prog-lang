import ply.lex as lex
from datetime import datetime
import os, random

# <<< INICIO APORTE Jose Chong

# Palabras reservadas
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

# Nombre de tokens (Los necesarios para poder hacer codigo validos con estructuras de control)
tokens = (
    'IDENTIFIER',
    'NUMBER',
    'STRING',

    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'SEMI_COLON',
    'COLON',
    'EQUAL',
    'ARROW',
    'QUESTION',

    'CLOSED_RANGE',
    'HALF_OPEN_RANGE',
    'DOT',
) + tuple(reserved.values())

# Descripcion de tokens sencillos
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMI_COLON = r';'
t_COLON = r':'
t_CLOSED_RANGE = r'\.\.\.'
t_HALF_OPEN_RANGE = r'\.\.<'
t_DOT = r'\.'
t_EQUAL = r'='
t_ARROW = r'->'
t_QUESTION = r'\?'

# Saltarse espacios y tabs
t_ignore = ' \t'

# Descripcion de tokens mas complejos
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

# Construcción del lexer
lexer = lex.lex()


def tokenize_code(code_str: str):
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
        # Formatear el valor para que sea legible
        valor_str = str(tk['value'])
        if len(valor_str) > 40:
            valor_str = valor_str[:37] + "..."

        log_lines.append(
            f"{tk['line']:>6} {tk['pos']:>6}  {tk['type']:>20}  {valor_str}"
        )

    log_lines.append("=" * 70)
    return "\n".join(log_lines)


def analizar_archivo_swift(ruta_archivo: str, github_user: str):
    print("=" * 70)
    print("ANALIZADOR LÉXICO DE SWIFT - ESTRUCTURAS DE CONTROL Y PALABRAS RESERVADAS")
    print("=" * 70)
    print(f"Archivo: {ruta_archivo}")
    print(f"Usuario: {github_user}\n")

    # Leer el archivo
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo_swift = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        print(f"Verifica que la ruta sea correcta.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Generar el contenido del log
    log_text = tokenize_and_dump(codigo_swift, github_user=github_user)

    # Crear carpeta logs/ si no existe
    os.makedirs("logs", exist_ok=True)

    # Formatear nombre con fecha/hora
    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    filename = f"logs/lexico-{github_user}-{timestamp}-{random.randint(100000,999999)}.txt"

    # Guardar el log
    with open(filename, "w", encoding="utf-8") as f:
        f.write(log_text)

    print(f"✅ Log guardado correctamente en: {filename}")
    print(f"   Total de tokens: {len(tokenize_code(codigo_swift))}")


if __name__ == "__main__":

    GITHUB_USER = "Jlchong3"
    ARCHIVOS_SWIFT = ["Examples/josechong_prueba_1.swift","Examples/josechong_prueba_2.swift"]

    for archivo in ARCHIVOS_SWIFT:
        analizar_archivo_swift(archivo, GITHUB_USER)

# <<< FIN APORTE Jose Chong
