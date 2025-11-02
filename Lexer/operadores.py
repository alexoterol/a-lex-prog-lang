import ply.lex as lex
import os
from datetime import datetime


# <<< INICIO APORTE Alexandre Icaza

# Lista de tokens
tokens = (
    # Operadores aritméticos
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    
    # Operadores de comparación
    'EQ', # ==
    'NE', # !=
    'GT', # >
    'LT', # <
    'GE', # >=
    'LE', # <=
    
    # Operadores de asignación
    'ASSIGN', # =
    'PLUS_ASSIGN', # +=
    'MINUS_ASSIGN', # -=
    'TIMES_ASSIGN', # *=
    'DIV_ASSIGN', # /=
    'MOD_ASSIGN', # %=
    
    # Operadores lógicos
    'NOT', # !
    'AND', # &&
    'OR', # ||
    
    # Operadores ternario y nil-coalescing
    'QUESTION', # ?
    'COLON', # :
    'NIL_COALESCE', # ??
    
    # Operadores de rango
    'CLOSED_RANGE', # ...
    'HALF_OPEN_RANGE', # ..<
    
    # Otros tokens necesarios
    'NUMBER',
    'IDENTIFIER',
)

# Estados para comentarios multilínea
states = (
    ('comment', 'exclusive'),
)


# Reglas de expresiones regulares para tokens

# Comentarios de documentación (///) - IGNORAR
def t_COMMENT_DOC(t):
    r'///.*'
    pass

# Comentario de línea simple (//) - IGNORAR
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

# Comentario multilínea (/* ... */ y /** ... */) - IGNORAR
def t_comment(t):
    r'/\*'
    t.lexer.push_state('comment')

def t_comment_end(t):
    r'\*/'
    t.lexer.pop_state()
    pass


def t_comment_content(t):
    r'[^*\n]+'
    pass

def t_comment_star(t):
    r'\*'
    pass

def t_comment_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_comment_error(t):
    t.lexer.skip(1)


# Operadores de rango
t_CLOSED_RANGE = r'\.\.\.'
t_HALF_OPEN_RANGE = r'\.\.<'

# Operadores de asignación compuesta
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='

# Operadores de comparación
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_LE = r'<='

# Operadores lógicos
t_AND = r'&&'
t_OR = r'\|\|'

# Nil-coalescing
t_NIL_COALESCE = r'\?\?'

# Operadores simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_GT = r'>'
t_LT = r'<'
t_ASSIGN = r'='
t_NOT = r'!'
t_QUESTION = r'\?'
t_COLON = r':'

# Números
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    pass # Para el tercer log decidí ignorar para evidenciar solo los operadores (Para los dos primeros logs si los reconocía)

# Identificadores
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    pass # # Para el tercer log decidí ignorar para evidenciar solo los operadores (Para los dos primeros logs si los reconocía)

# Espacios en blanco y tabulaciones
t_ignore = ' \t'
t_comment_ignore = ''

# Nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
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
    print("ANALIZADOR LÉXICO DE SWIFT - OPERADORES Y COMENTARIOS")
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
    filename = f"logs/lexico-{github_user}-{timestamp}.txt"
    
    # Guardar el log
    with open(filename, "w", encoding="utf-8") as f:
        f.write(log_text)
    
    print(f"✅ Log guardado correctamente en: {filename}")
    print(f"   Total de tokens: {len(tokenize_code(codigo_swift))}")


if __name__ == "__main__":    
    
    GITHUB_USER = "aledicaz"
    ARCHIVO_SWIFT = "Examples/alexandre.swift"
    

    analizar_archivo_swift(ARCHIVO_SWIFT, GITHUB_USER)

# <<< FIN APORTE Alexandre Icaza