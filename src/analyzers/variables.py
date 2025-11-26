"""
VARIABLES / DECLARACIONES
Alex Otero
"""

import ply.lex as lex
from datetime import datetime

# >>> Alex Otero

reserved = {
    'let':    'LET',
    'var':    'VAR',

    # Tipos básicos comunes en declaraciones
    'Int':    'TYPE_INT',
    'String': 'TYPE_STRING',
    'Double': 'TYPE_DOUBLE',
    'Bool':   'TYPE_BOOL',
    'nil':    'NIL',
}

tokens = [
    'LET',
    'VAR',
    'TYPE_INT',
    'TYPE_STRING',
    'TYPE_DOUBLE',
    'TYPE_BOOL',
    'NIL',

    'IDENTIFIER',

    'INT_LITERAL',
    'FLOAT_LITERAL',
    'STRING_LITERAL',

    'ASSIGN',      # =
    'COLON',       # :
    'COMMA',       # ,
    'QUESTION',    # ?
    'BANG',        # !

    'NEWLINE',
]

t_ASSIGN   = r'='
t_COLON    = r':'
t_COMMA    = r','
t_QUESTION = r'\?'
t_BANG     = r'!'

# STRING_LITERAL
string_pattern = r'"([^"\n]|(\\"))*"'
t_STRING_LITERAL = string_pattern

# Ignorar espacios y tabs
t_ignore = ' \t\r'

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    # Ej: 3.14, 0.0, 12.0
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    token_type = reserved.get(t.value)
    if token_type:
        t.type = token_type
    return t

def t_comment_singleline(t):
    r'//[^\n]*'
    pass

def t_comment_multiline(t):
    r'/\*([^*]|\*+[^/])*\*+/'
    pass

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    err_text = f"[LEX ERROR] Línea {t.lexer.lineno}, Char '{t.value[0]}' no reconocido"
    t.value = err_text
    t.type = 'LEX_ERROR'
    t.lexer.skip(1)
    return t

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
    header = f"LEXICO | usuario={github_user} | fecha-hora={timestamp}\n"
    log_lines.append(header)
    log_lines.append("-" * len(header))

    for tk in tokens_list:
        log_lines.append(
            f"{tk['line']:>3}:{tk['pos']:<4}  {tk['type']:>12}  {tk['value']}"
        )

    return "\n".join(log_lines)

if __name__ == "__main__":
    # Ejemplo de código Swift para probar tu lexer
    swift_sample = '''
    let maxCount = 10
    var name: String = "Ana"
    var score: Bool = True
    var optionalName: String? = nil
    var x = 0, y = 1, z = 2
    '''

    # Tu usuario Git (ajústalo)
    user_git = "alexoterol"

    # Generar el contenido del log
    log_text = tokenize_and_dump(swift_sample, github_user=user_git)

    # Crear carpeta logs/ si no existe
    import os
    os.makedirs("logs", exist_ok=True)

    # Formatear nombre con fecha/hora
    from datetime import datetime
    timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    filename = f"logs/lexico-{user_git}-{timestamp}.txt"

    # Guardar el log
    with open(filename, "w", encoding="utf-8") as f:
        f.write(log_text)

    print(f"✅ Log guardado correctamente en: {filename}")

# <<< FIN APORTE Alex Otero
