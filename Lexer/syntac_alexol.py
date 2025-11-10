import ply.yacc as yacc
import os
import shutil
from datetime import datetime
from contextlib import redirect_stdout

# Importar tokens del lexer global
from analizador_lex import tokens, lexer

"""
🟩 ANALIZADOR SINTÁCTICO - SWIFT - INTEGRANTE 2
Control de Flujo y Lógica

Responsabilidades:
1. Expresiones booleanas y operadores lógicos (&&, ||, !)
2. Operador ternario (? :) y Nil-coalescing (??)
3. Condicionales if-else, if-else if-else, guard
4. Diccionarios [String: Int], [String: Any]
5. Bucle while
6. Funciones con parámetros opcionales y valores por defecto
"""

# PRECEDENCIA DE OPERADORES (heredada y extendida)
precedence = (
    ('right', 'QUESTION', 'COLON'),  # Ternario
    ('left', 'NIL_COALESCE'),        # ??
    ('left', 'OR'),                  # ||
    ('left', 'AND'),                 # &&
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS', 'UPLUS', 'NOT'),
)


# ============================================================================
# REGLA INICIAL
# ============================================================================
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])
    print("✓ Programa válido")


def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    '''statement : variable_declaration
                 | assignment
                 | if_statement
                 | guard_statement
                 | while_statement
                 | function_declaration
                 | expression_statement
                 | return_statement
                 | NEWLINE'''
    if p[1] != '\n':
        p[0] = p[1]


# ============================================================================
# DECLARACIÓN DE VARIABLES (incluyendo diccionarios)
# ============================================================================
def p_variable_declaration(p):
    '''variable_declaration : LET IDENTIFIER COLON type_annotation ASSIGN expression
                           | VAR IDENTIFIER COLON type_annotation ASSIGN expression
                           | LET IDENTIFIER ASSIGN expression
                           | VAR IDENTIFIER ASSIGN expression'''
    if len(p) == 7:
        p[0] = ('var_decl', p[1], p[2], p[4], p[6])
        print(f"✓ Declaración de variable: {p[1]} {p[2]}: {p[4]} = ...")
    else:
        p[0] = ('var_decl', p[1], p[2], None, p[4])
        print(f"✓ Declaración de variable: {p[1]} {p[2]} = ...")


def p_type_annotation(p):
    '''type_annotation : TYPE_INT
                       | TYPE_DOUBLE
                       | TYPE_BOOL
                       | TYPE_STRING
                       | dictionary_type
                       | optional_type'''
    p[0] = p[1]


def p_optional_type(p):
    '''optional_type : TYPE_INT QUESTION
                     | TYPE_DOUBLE QUESTION
                     | TYPE_BOOL QUESTION
                     | TYPE_STRING QUESTION'''
    p[0] = ('optional_type', p[1])
    print(f"✓ Tipo opcional: {p[1]}?")


def p_dictionary_type(p):
    '''dictionary_type : LBRACKET type_annotation COLON type_annotation RBRACKET'''
    p[0] = ('dict_type', p[2], p[4])
    print(f"✓ Tipo diccionario: [{p[2]}: {p[4]}]")


# ============================================================================
# ASIGNACIÓN
# ============================================================================
def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression'''
    p[0] = ('assignment', p[1], p[3])
    print(f"✓ Asignación: {p[1]} = ...")


# ============================================================================
# EXPRESIONES BOOLEANAS Y LÓGICAS
# ============================================================================
def p_expression_logical(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = ('logical', p[2], p[1], p[3])
    print(f"✓ Expresión lógica: ... {p[2]} ...")


def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = ('not', p[2])
    print(f"✓ Negación lógica: !...")


def p_expression_comparison(p):
    '''expression : expression EQ expression
                  | expression NE expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression'''
    p[0] = ('comparison', p[2], p[1], p[3])
    print(f"✓ Expresión de comparación: ... {p[2]} ...")


def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression'''
    p[0] = ('binop', p[2], p[1], p[3])
    print(f"✓ Expresión aritmética: ... {p[2]} ...")


def p_expression_unary(p):
    '''expression : MINUS expression %prec UMINUS
                  | PLUS expression %prec UPLUS'''
    p[0] = ('unary', p[1], p[2])


def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


# ============================================================================
# OPERADOR TERNARIO
# ============================================================================
def p_expression_ternary(p):
    '''expression : expression QUESTION expression COLON expression'''
    p[0] = ('ternary', p[1], p[3], p[5])
    print(f"✓ Operador ternario: ... ? ... : ...")


# ============================================================================
# NIL-COALESCING OPERATOR (??)
# ============================================================================
def p_expression_nil_coalescing(p):
    '''expression : expression NIL_COALESCE expression'''
    p[0] = ('nil_coalesce', p[1], p[3])
    print(f"✓ Operador nil-coalescing: ... ?? ...")


# ============================================================================
# LITERALES Y VALORES
# ============================================================================
def p_expression_literal(p):
    '''expression : INT_LITERAL
                  | FLOAT_LITERAL
                  | STRING
                  | TRUE
                  | FALSE
                  | NIL'''
    p[0] = ('literal', p[1])


def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = ('identifier', p[1])


def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ('expr_stmt', p[1])


# ============================================================================
# DICCIONARIOS - ESTRUCTURA DE DATOS
# ============================================================================
def p_expression_dictionary_literal(p):
    '''expression : LBRACKET dictionary_pairs RBRACKET
                  | LBRACKET COLON RBRACKET'''
    if len(p) == 4 and p[2] == ':':
        p[0] = ('dict_literal', [])
        print("✓ Diccionario vacío: [:]")
    else:
        p[0] = ('dict_literal', p[2])
        print(f"✓ Diccionario literal: [{len(p[2])} pares]")


def p_dictionary_pairs(p):
    '''dictionary_pairs : dictionary_pairs COMMA dictionary_pair
                        | dictionary_pair'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_dictionary_pair(p):
    '''dictionary_pair : expression COLON expression'''
    p[0] = ('dict_pair', p[1], p[3])


def p_expression_dictionary_access(p):
    '''expression : IDENTIFIER LBRACKET expression RBRACKET'''
    p[0] = ('dict_access', p[1], p[3])
    print(f"✓ Acceso a diccionario: {p[1]}[...]")


# ============================================================================
# CONDICIONALES IF-ELSE
# ============================================================================
def p_if_statement(p):
    '''if_statement : IF expression LBRACE statement_list RBRACE
                    | IF expression LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
                    | IF expression LBRACE statement_list RBRACE else_if_chain
                    | IF expression LBRACE statement_list RBRACE else_if_chain ELSE LBRACE statement_list RBRACE'''
    if len(p) == 6:
        p[0] = ('if', p[2], p[4], None, None)
        print(f"✓ Condicional if")
    elif len(p) == 10 and p[6] == 'else':
        p[0] = ('if_else', p[2], p[4], p[8])
        print(f"✓ Condicional if-else")
    elif len(p) == 7:
        p[0] = ('if_elif', p[2], p[4], p[6], None)
        print(f"✓ Condicional if-else if")
    else:
        p[0] = ('if_elif_else', p[2], p[4], p[6], p[9])
        print(f"✓ Condicional if-else if-else")


def p_else_if_chain(p):
    '''else_if_chain : else_if_chain else_if_statement
                     | else_if_statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_else_if_statement(p):
    '''else_if_statement : ELSE IF expression LBRACE statement_list RBRACE'''
    p[0] = ('else_if', p[3], p[5])
    print(f"✓ else if")


# ============================================================================
# GUARD STATEMENT
# ============================================================================
def p_guard_statement(p):
    '''guard_statement : GUARD expression ELSE LBRACE statement_list RBRACE'''
    p[0] = ('guard', p[2], p[5])
    print(f"✓ Guard statement")


# ============================================================================
# WHILE LOOP
# ============================================================================
def p_while_statement(p):
    '''while_statement : WHILE expression LBRACE statement_list RBRACE'''
    p[0] = ('while', p[2], p[4])
    print(f"✓ Bucle while")


# ============================================================================
# FUNCIONES CON PARÁMETROS OPCIONALES Y VALORES POR DEFECTO
# ============================================================================
def p_function_declaration(p):
    '''function_declaration : FUNC IDENTIFIER LPAREN parameter_list RPAREN ARROW type_annotation LBRACE statement_list RBRACE
                           | FUNC IDENTIFIER LPAREN RPAREN ARROW type_annotation LBRACE statement_list RBRACE
                           | FUNC IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                           | FUNC IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 11:
        p[0] = ('func_decl', p[2], p[4], p[7], p[9])
        print(f"✓ Función: func {p[2]}({len(p[4])} parámetros) -> {p[7]}")
    elif len(p) == 10:
        p[0] = ('func_decl', p[2], [], p[6], p[8])
        print(f"✓ Función: func {p[2]}() -> {p[6]}")
    elif len(p) == 9:
        p[0] = ('func_decl', p[2], p[4], None, p[7])
        print(f"✓ Función: func {p[2]}({len(p[4])} parámetros)")
    else:
        p[0] = ('func_decl', p[2], [], None, p[6])
        print(f"✓ Función: func {p[2]}()")


def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_parameter(p):
    '''parameter : IDENTIFIER COLON type_annotation
                 | IDENTIFIER COLON type_annotation ASSIGN expression'''
    if len(p) == 4:
        p[0] = ('param', p[1], p[3], None)
    else:
        p[0] = ('param_default', p[1], p[3], p[5])
        print(f"✓ Parámetro con valor por defecto: {p[1]}")


def p_return_statement(p):
    '''return_statement : RETURN expression
                        | RETURN'''
    if len(p) == 3:
        p[0] = ('return', p[2])
        print(f"✓ Return con valor")
    else:
        p[0] = ('return', None)
        print("✓ Return")


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================
def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en línea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"
        print(f"❌ {error_msg}")
    else:
        error_msg = "Error de sintaxis: Final de archivo inesperado"
        print(f"❌ {error_msg}")


# ============================================================================
# CONSTRUCCIÓN DEL PARSER
# ============================================================================
parser = yacc.yacc()


# ============================================================================
# FUNCIÓN PARA ANALIZAR ARCHIVO Y COPIAR LOG
# ============================================================================
def analizar_archivo_swift(ruta_archivo: str, github_user: str):
    """
    Lee un archivo Swift, lo analiza y copia el parser.out a logs/
    """
    print("=" * 70)
    print("ANALIZADOR SINTÁCTICO DE SWIFT - INTEGRANTE 2")
    print("Control de Flujo y Lógica")
    print("=" * 70)
    print(f"Archivo: {ruta_archivo}")
    print(f"Usuario: {github_user}\n")
    
    # Leer archivo
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{ruta_archivo}'")
        return
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # --- MODIFICACIÓN CLAVE: Redirigir la salida a parser.out ---
    parser_out_path = "parser.out"
    print("Analizando sintaxis y capturando log de parser en 'parser.out'...\n")
    
    # 1. Redirige la salida estándar (stdout) al archivo 'parser.out'
    try:
        with open(parser_out_path, 'w', encoding='utf-8') as f_out:
            with redirect_stdout(f_out):
                # 2. El parser debe ser llamado *dentro* del bloque de redirección.
                # Si tu parser de PLY escribe la tabla de gramática y estados 
                # (como la que mostraste) usando la función 'output', esta llamada 
                # asegurará que esa salida se escriba en f_out (parser.out).
                result = parser.parse(codigo, lexer=lexer) 
        
        # Este print vuelve a la consola normal (sys.stdout) una vez fuera del 'with'
        print("\n✓ Análisis sintáctico completado")
        
    except Exception as e:
        # Los errores de excepción se imprimirán en la consola normal
        print(f"\n❌ Error durante el análisis: {e}")
    # -------------------------------------------------------------------
    
    # Crear carpeta logs/ si no existe
    os.makedirs("logs", exist_ok=True)
    
    # Copiar parser.out a logs/ con el nombre correcto
    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f"logs/sintactico-{github_user}-{timestamp}.txt"
    
    try:
        # Ahora el archivo parser.out debe existir
        if os.path.exists(parser_out_path):
            shutil.copy(parser_out_path, log_filename)
            print(f"\n✓ Log guardado en: {log_filename}")
            # Opcional: Eliminar el archivo temporal 'parser.out' después de copiarlo
            # os.remove(parser_out_path)
        else:
            print(f"\n⚠️ Advertencia: No se encontró {parser_out_path}. El parser no lo generó.")
    except Exception as e:
        print(f"\n❌ Error al copiar log: {e}")
    
    print("=" * 70)


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    GITHUB_USER = "alexoterol"  # Cambia esto por tu usuario
    ARCHIVO_SWIFT = "Examples/alexotero_prueba_synt.swift"
    
    analizar_archivo_swift(ARCHIVO_SWIFT, GITHUB_USER)