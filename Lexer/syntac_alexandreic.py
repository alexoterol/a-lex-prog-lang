import ply.yacc as yacc
import os
import shutil
from datetime import datetime
import time

# Importar tokens del lexer global
from analizador_lex import tokens, lexer

# <<< INICIO APORTE Alexandre Icaza

"""
ANALIZADOR SINTÁCTICO - SWIFT
Integrante: Alexandre Icaza (aledicaz)

Responsabilidades:
1. Expresiones aritméticas con operadores
2. Declaración y asignación de variables (let/var)
3. Estructura de Datos: Arrays
4. Estructura de Control: for-in
5. Funciones simples con parámetros y retorno
"""

# PRECEDENCIA DE OPERADORES
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS', 'UPLUS', 'NOT'),
)


# REGLA INICIAL
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
                 | for_statement
                 | function_declaration
                 | expression_statement
                 | NEWLINE'''
    if p[1] != '\n':
        p[0] = p[1]


# DECLARACIÓN DE VARIABLES
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
                       | array_type'''
    p[0] = p[1]

def p_array_type(p):
    '''array_type : LBRACKET type_annotation RBRACKET'''
    p[0] = ('array_type', p[2])
    print(f"✓ Tipo array: [{p[2]}]")


# ASIGNACIÓN DE VARIABLES
def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression
                  | IDENTIFIER PLUS_ASSIGN expression
                  | IDENTIFIER MINUS_ASSIGN expression
                  | IDENTIFIER TIMES_ASSIGN expression
                  | IDENTIFIER DIV_ASSIGN expression
                  | IDENTIFIER MOD_ASSIGN expression'''
    p[0] = ('assignment', p[1], p[2], p[3])
    print(f"✓ Asignación: {p[1]} {p[2]} ...")


# EXPRESIONES ARITMÉTICAS
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression'''
    p[0] = ('binop', p[2], p[1], p[3])
    print(f"✓ Expresión aritmética: ... {p[2]} ...")

def p_expression_comparison(p):
    '''expression : expression EQ expression
                  | expression NE expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression'''
    p[0] = ('comparison', p[2], p[1], p[3])
    print(f"✓ Expresión de comparación: ... {p[2]} ...")

def p_expression_unary(p):
    '''expression : MINUS expression %prec UMINUS
                  | PLUS expression %prec UPLUS'''
    p[0] = ('unary', p[1], p[2])
    print(f"✓ Expresión unaria: {p[1]}...")

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_literal(p):
    '''expression : INT_LITERAL
                  | FLOAT_LITERAL
                  | STRING
                  | TRUE
                  | FALSE'''
    p[0] = ('literal', p[1])

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = ('identifier', p[1])

def p_expression_array_access(p):
    '''expression : IDENTIFIER LBRACKET expression RBRACKET'''
    p[0] = ('array_access', p[1], p[3])
    print(f"✓ Acceso a array: {p[1]}[...]")

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ('expr_stmt', p[1])



# ARRAYS - ESTRUCTURA DE DATOS
def p_expression_array_literal(p):
    '''expression : LBRACKET array_elements RBRACKET
                  | LBRACKET RBRACKET'''
    if len(p) == 4:
        p[0] = ('array_literal', p[2])
        print(f"✓ Array literal: [{len(p[2])} elementos]")
    else:
        p[0] = ('array_literal', [])
        print("✓ Array vacío: []")

def p_array_elements(p):
    '''array_elements : array_elements COMMA expression
                      | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]



# FOR-IN LOOP - ESTRUCTURA DE CONTROL
def p_for_statement(p):
    '''for_statement : FOR IDENTIFIER IN range_expression LBRACE statement_list RBRACE
                     | FOR IDENTIFIER IN expression LBRACE statement_list RBRACE'''
    p[0] = ('for_in', p[2], p[4], p[6])
    print(f"✓ Bucle for-in: for {p[2]} in ...")

def p_range_expression(p):
    '''range_expression : expression CLOSED_RANGE expression
                        | expression HALF_OPEN_RANGE expression'''
    p[0] = ('range', p[2], p[1], p[3])
    print(f"✓ Rango: ... {p[2]} ...")



# FUNCIONES
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
    '''parameter : IDENTIFIER COLON type_annotation'''
    p[0] = ('param', p[1], p[3])

def p_statement_return(p):
    '''statement : RETURN expression
                 | RETURN'''
    if len(p) == 3:
        p[0] = ('return', p[2])
        print(f"✓ Return con valor")
    else:
        p[0] = ('return', None)
        print("✓ Return")


# MANEJO DE ERRORES
def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en línea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"
        print(f"❌ {error_msg}")
    else:
        error_msg = "Error de sintaxis: Final de archivo inesperado"
        print(f"❌ {error_msg}")



# CONSTRUCCIÓN DEL PARSER
parser = yacc.yacc()


# FUNCIÓN PARA ANALIZAR ARCHIVO Y COPIAR LOG
def analizar_archivo_swift(ruta_archivo: str, github_user: str):
    """
    Lee un archivo Swift, lo analiza y copia el parser.out a logs/
    """
    print("=" * 70)
    print("ANALIZADOR SINTÁCTICO DE SWIFT - Alexandre Icaza")
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
    
    # Analizar sintaxis
    print("Analizando sintaxis...\n")
    try:
        result = parser.parse(codigo, lexer=lexer)
        print("\n✓ Análisis sintáctico completado")
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
    
    # Crear carpeta logs/ si no existe
    os.makedirs("logs", exist_ok=True)
    
    #time.sleep(5)
    # Copiar parser.out a logs/ con el nombre correcto
    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f"logs/sintactico-{github_user}-{timestamp}.txt"
    
    try:
        if os.path.exists("Lexer/parser.out"):
            shutil.copy("Lexer/parser.out", log_filename)
            print(f"\n✓ Log guardado en: {log_filename}")
        else:
            print(f"\n⚠️  Advertencia: No se encontró parser.out")
    except Exception as e:
        print(f"\n❌ Error al copiar log: {e}")
    
    print("=" * 70)


# MAIN
if __name__ == "__main__":
    GITHUB_USER = "aledicaz"
    ARCHIVO_SWIFT = "Examples/alexandre_sintactico.swift"
    
    analizar_archivo_swift(ARCHIVO_SWIFT, GITHUB_USER)

# <<< FIN APORTE Alexandre Icaza