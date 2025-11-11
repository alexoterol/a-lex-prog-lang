import ply.yacc as yacc
import os
import shutil
from datetime import datetime

# Importar tokens del lexer global
from analizador_lex import tokens, lexer

"""
ANALIZADOR SINTÁCTICO GLOBAL - SWIFT
Proyecto de Lenguajes de Programación

INTEGRANTES:
1. Alexandre Icaza (aledicaz) - Expresiones aritméticas, Variables, Arrays, for-in, Funciones
2. Alex Otero (alexoterol) - Control de flujo, Lógica, Diccionarios, while, Guard, Operadores especiales
3. Jose Chong (Jlchong3) - Entrada/Salida, POO, Tuplas, Switch-case

ANÁLISIS SINTÁCTICO COMPLETO DE SWIFT
"""

# ============================================================================
# PRECEDENCIA DE OPERADORES (UNIFICADA)
# ============================================================================
precedence = (
    ('right', 'QUESTION', 'COLON'),  # Ternario
    ('left', 'NIL_COALESCE'),        # ??
    ('left', 'OR'),                  # ||
    ('left', 'AND'),                 # &&
    ('left', 'EQ', 'NE'),            # == !=
    ('left', 'LT', 'LE', 'GT', 'GE'), # < <= > >=
    ('left', 'PLUS', 'MINUS'),       # + -
    ('left', 'TIMES', 'DIVIDE', 'MODULO'), # * / %
    ('right', 'UMINUS', 'UPLUS', 'NOT'),   # unarios
)


# ============================================================================
# REGLA INICIAL Y ESTRUCTURA DEL PROGRAMA
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
                 | for_statement
                 | if_statement
                 | guard_statement
                 | while_statement
                 | switch_statement
                 | function_declaration
                 | function_call_statement
                 | class_declaration
                 | expression_statement
                 | return_statement
                 | NEWLINE'''
    if p[1] != '\n':
        p[0] = p[1]


def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ('expr_stmt', p[1])


# ============================================================================
# DECLARACIÓN DE VARIABLES (Alexandre + Alex O)
# ============================================================================
def p_variable_declaration(p):
    '''variable_declaration : LET IDENTIFIER COLON type_annotation ASSIGN expression
                           | VAR IDENTIFIER COLON type_annotation ASSIGN expression
                           | LET IDENTIFIER ASSIGN expression
                           | VAR IDENTIFIER ASSIGN expression
                           | LET IDENTIFIER COLON type_annotation
                           | VAR IDENTIFIER COLON type_annotation
                           | LET IDENTIFIER COLON tuple_type
                           | VAR IDENTIFIER COLON tuple_type'''
    if len(p) == 7:
        p[0] = ('var_decl', p[1], p[2], p[4], p[6])
        print(f"✓ Declaración de variable: {p[1]} {p[2]}: {p[4]} = ...")
    elif len(p) == 5 and p[3] == ':':
        p[0] = ('var_decl', p[1], p[2], p[4], None)
        print(f"✓ Declaración de variable: {p[1]} {p[2]}: {p[4]}")
    else:
        p[0] = ('var_decl', p[1], p[2], None, p[4])
        print(f"✓ Declaración de variable: {p[1]} {p[2]} = ...")


def p_type_annotation(p):
    '''type_annotation : TYPE_INT
                       | TYPE_DOUBLE
                       | TYPE_BOOL
                       | TYPE_STRING
                       | array_type
                       | dictionary_type
                       | optional_type
                       | tuple_type
                       | IDENTIFIER'''
    p[0] = p[1]


def p_optional_type(p):
    '''optional_type : TYPE_INT QUESTION
                     | TYPE_DOUBLE QUESTION
                     | TYPE_BOOL QUESTION
                     | TYPE_STRING QUESTION'''
    p[0] = ('optional_type', p[1])
    print(f"✓ Tipo opcional: {p[1]}?")


# ============================================================================
# ARRAYS (Alexandre)
# ============================================================================
def p_array_type(p):
    '''array_type : LBRACKET type_annotation RBRACKET'''
    p[0] = ('array_type', p[2])
    print(f"✓ Tipo array: [{p[2]}]")


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


def p_expression_array_access(p):
    '''expression : expression LBRACKET expression RBRACKET'''
    p[0] = ('subscript_access', p[1], p[3])
    print(f"✓ Acceso con subíndice: ...[...]")


# ============================================================================
# DICCIONARIOS (Alex O)
# ============================================================================
def p_dictionary_type(p):
    '''dictionary_type : LBRACKET type_annotation COLON type_annotation RBRACKET'''
    p[0] = ('dict_type', p[2], p[4])
    print(f"✓ Tipo diccionario: [{p[2]}: {p[4]}]")


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


# ============================================================================
# TUPLAS (Jose)
# ============================================================================
def p_tuple_type(p):
    '''tuple_type : LPAREN tuple_type_elements RPAREN'''
    p[0] = ('tuple_type', p[2])
    print(f"✓ Tipo tupla con {len(p[2])} elementos")


def p_tuple_type_elements(p):
    '''tuple_type_elements : tuple_type_elements COMMA tuple_type_element
                           | tuple_type_element'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_tuple_type_element(p):
    '''tuple_type_element : IDENTIFIER COLON type_annotation
                          | type_annotation'''
    if len(p) == 4:
        p[0] = ('named_type', p[1], p[3])
    else:
        p[0] = p[1]


def p_expression_tuple(p):
    '''expression : LPAREN tuple_elements RPAREN'''
    p[0] = ('tuple', p[2])
    print(f"✓ Tupla con {len(p[2])} elementos")


def p_tuple_elements(p):
    '''tuple_elements : tuple_elements COMMA tuple_element
                      | tuple_element'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_tuple_element(p):
    '''tuple_element : IDENTIFIER COLON expression
                     | expression'''
    if len(p) == 4:
        p[0] = ('named_element', p[1], p[3])
        print(f"✓ Elemento nombrado: {p[1]}")
    else:
        p[0] = p[1]


def p_expression_tuple_access(p):
    '''expression : expression DOT INT_LITERAL'''
    p[0] = ('tuple_access', p[1], p[3])
    print(f"✓ Acceso a tupla por índice: .{p[3]}")


def p_expression_member_access(p):
    '''expression : expression DOT IDENTIFIER'''
    p[0] = ('member_access', p[1], p[3])
    print(f"✓ Acceso a miembro: .{p[3]}")


# ============================================================================
# ASIGNACIÓN (Alexandre + Alex O) - CORREGIDA PARA SOPORTAR EXPRESIONES
# ============================================================================
def p_assignment(p):
    '''assignment : lvalue ASSIGN expression
                  | lvalue PLUS_ASSIGN expression
                  | lvalue MINUS_ASSIGN expression
                  | lvalue TIMES_ASSIGN expression
                  | lvalue DIV_ASSIGN expression
                  | lvalue MOD_ASSIGN expression'''
    p[0] = ('assignment', p[1], p[2], p[3])
    print(f"✓ Asignación: ... {p[2]} ...")


def p_lvalue(p):
    '''lvalue : IDENTIFIER
              | SELF DOT IDENTIFIER
              | lvalue DOT IDENTIFIER
              | lvalue LBRACKET expression RBRACKET'''
    if len(p) == 2:
        p[0] = ('identifier', p[1])
    elif len(p) == 4 and p[2] == '.':
        p[0] = ('member_access', p[1], p[3])
    else:
        p[0] = ('subscript_access', p[1], p[3])


# ============================================================================
# EXPRESIONES ARITMÉTICAS (Alexandre)
# ============================================================================
def p_expression_binop(p):
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
    print(f"✓ Expresión unaria: {p[1]}...")


# ============================================================================
# EXPRESIONES LÓGICAS Y BOOLEANAS (Alex O)
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


# ============================================================================
# OPERADOR TERNARIO Y NIL-COALESCING (Alex O)
# ============================================================================
def p_expression_ternary(p):
    '''expression : expression QUESTION expression COLON expression'''
    p[0] = ('ternary', p[1], p[3], p[5])
    print(f"✓ Operador ternario: ... ? ... : ...")


def p_expression_nil_coalescing(p):
    '''expression : expression NIL_COALESCE expression'''
    p[0] = ('nil_coalesce', p[1], p[3])
    print(f"✓ Operador nil-coalescing: ... ?? ...")


# ============================================================================
# EXPRESIONES BÁSICAS Y LITERALES
# ============================================================================
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


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


def p_expression_self_access(p):
    '''expression : SELF DOT IDENTIFIER'''
    p[0] = ('self_access', p[3])
    print(f"✓ Acceso a propiedad: self.{p[3]}")


# ============================================================================
# LLAMADAS A FUNCIÓN COMO EXPRESIÓN (CORREGIDO)
# ============================================================================
def p_expression_function_call(p):
    '''expression : IDENTIFIER LPAREN argument_list RPAREN
                  | IDENTIFIER LPAREN RPAREN'''
    function_name = p[1]
    
    if len(p) == 5:
        arguments = p[3]
        p[0] = ('function_call', function_name, arguments)
    else:
        p[0] = ('function_call', function_name, [])


# ============================================================================
# ESTRUCTURA DE CONTROL: FOR-IN (Alexandre)
# ============================================================================
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


# ============================================================================
# ESTRUCTURA DE CONTROL: IF-ELSE (Alex O)
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
# ESTRUCTURA DE CONTROL: GUARD (Alex O)
# ============================================================================
def p_guard_statement(p):
    '''guard_statement : GUARD expression ELSE LBRACE statement_list RBRACE'''
    p[0] = ('guard', p[2], p[5])
    print(f"✓ Guard statement")


# ============================================================================
# ESTRUCTURA DE CONTROL: WHILE (Alex O)
# ============================================================================
def p_while_statement(p):
    '''while_statement : WHILE expression LBRACE statement_list RBRACE'''
    p[0] = ('while', p[2], p[4])
    print(f"✓ Bucle while")


# ============================================================================
# ESTRUCTURA DE CONTROL: SWITCH-CASE (Jose)
# ============================================================================
def p_switch_statement(p):
    '''switch_statement : SWITCH expression LBRACE optional_newlines case_list optional_newlines RBRACE
                        | SWITCH expression LBRACE optional_newlines case_list default_case optional_newlines RBRACE'''
    if len(p) == 9:
        p[0] = ('switch', p[2], p[5], p[6])
        print(f"✓ Switch con {len(p[5])} caso(s) y default")
    else:
        p[0] = ('switch', p[2], p[5], None)
        print(f"✓ Switch con {len(p[5])} caso(s)")


def p_case_list(p):
    '''case_list : case_list optional_newlines case_clause
                 | optional_newlines case_clause'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[2]]


def p_case_clause(p):
    '''case_clause : CASE case_patterns COLON optional_newlines case_body'''
    p[0] = ('case', p[2], p[5])
    print(f"✓ Case con {len(p[2])} patrón(es)")


def p_case_body(p):
    '''case_body : statement_list'''
    p[0] = p[1]


def p_case_patterns(p):
    '''case_patterns : case_patterns COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_default_case(p):
    '''default_case : DEFAULT COLON optional_newlines case_body'''
    p[0] = ('default', p[4])
    print("✓ Default case")


def p_optional_newlines(p):
    '''optional_newlines : optional_newlines NEWLINE
                         | empty'''
    pass


# ============================================================================
# FUNCIONES (Alexandre + Alex O)
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
# ENTRADA/SALIDA: PRINT Y READLINE (Jose) - COMO STATEMENT
# ============================================================================
def p_function_call_statement(p):
    '''function_call_statement : IDENTIFIER LPAREN argument_list RPAREN
                               | IDENTIFIER LPAREN RPAREN'''
    function_name = p[1]
    
    if len(p) == 5:
        arguments = p[3]
        if function_name == 'print':
            p[0] = ('print', arguments)
            print(f"✓ Print con {len(arguments)} argumento(s)")
        elif function_name == 'readLine':
            if len(arguments) <= 1:
                p[0] = ('readline', arguments[0] if arguments else None)
                print(f"✓ Lectura de entrada: readLine()")
            else:
                print(f"❌ Error: readLine() solo acepta 0 o 1 argumento(s)")
                p[0] = ('error', 'readLine con argumentos incorrectos')
        else:
            p[0] = ('function_call', function_name, arguments)
            print(f"✓ Llamada a función: {function_name}()")
    else:
        if function_name == 'print':
            p[0] = ('print', [])
            print("✓ Print vacío")
        elif function_name == 'readLine':
            p[0] = ('readline', None)
            print("✓ Lectura de entrada: readLine()")
        else:
            p[0] = ('function_call', function_name, [])
            print(f"✓ Llamada a función: {function_name}()")


def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


# ============================================================================
# POO: CLASES (Jose)
# ============================================================================
def p_class_declaration(p):
    '''class_declaration : CLASS IDENTIFIER LBRACE class_body RBRACE'''
    p[0] = ('class_decl', p[2], p[4])
    print(f"✓ Clase: class {p[2]}")


def p_class_body(p):
    '''class_body : class_body class_member
                 | class_member
                 | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_class_member(p):
    '''class_member : property_declaration
                   | init_declaration
                   | method_declaration
                   | computed_property
                   | NEWLINE'''
    if p[1] != '\n':
        p[0] = p[1]


def p_property_declaration(p):
    '''property_declaration : VAR IDENTIFIER COLON type_annotation
                           | LET IDENTIFIER COLON type_annotation
                           | VAR IDENTIFIER COLON tuple_type
                           | LET IDENTIFIER COLON tuple_type'''
    p[0] = ('property', p[1], p[2], p[4])
    print(f"✓ Propiedad: {p[1]} {p[2]}: {p[4]}")


def p_computed_property(p):
    '''computed_property : VAR IDENTIFIER COLON type_annotation LBRACE optional_newlines GET LBRACE optional_newlines statement_list optional_newlines RBRACE optional_newlines RBRACE'''
    p[0] = ('computed_property', p[2], p[4], p[10])
    print(f"✓ Propiedad computada: var {p[2]}: {p[4]}")


def p_init_declaration(p):
    '''init_declaration : INIT LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                        | INIT LPAREN RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 8:
        p[0] = ('init', p[3], p[6])
        print(f"✓ Inicializador: init({len(p[3])} parámetros)")
    else:
        p[0] = ('init', [], p[5])
        print("✓ Inicializador: init()")


def p_method_declaration(p):
    '''method_declaration : FUNC IDENTIFIER LPAREN parameter_list RPAREN ARROW type_annotation LBRACE statement_list RBRACE
                          | FUNC IDENTIFIER LPAREN RPAREN ARROW type_annotation LBRACE statement_list RBRACE
                          | FUNC IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                          | FUNC IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 11:
        p[0] = ('method', p[2], p[4], p[7], p[9])
        print(f"✓ Método: func {p[2]}({len(p[4])} parámetros) -> {p[7]}")
    elif len(p) == 10:
        p[0] = ('method', p[2], [], p[6], p[8])
        print(f"✓ Método: func {p[2]}() -> {p[6]}")
    elif len(p) == 9:
        p[0] = ('method', p[2], p[4], None, p[7])
        print(f"✓ Método: func {p[2]}({len(p[4])} parámetros)")
    else:
        p[0] = ('method', p[2], [], None, p[6])
        print(f"✓ Método: func {p[2]}()")


# ============================================================================
# AUXILIARES
# ============================================================================
def p_empty(p):
    '''empty :'''
    pass


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
    print("ANALIZADOR SINTÁCTICO GLOBAL DE SWIFT")
    print("Proyecto de Lenguajes de Programación")
    print("=" * 70)
    print("Integrantes:")
    print("  - Alexandre Icaza (aledicaz)")
    print("  - Alex Otero (alexoterol)")
    print("  - Jose Chong (Jlchong3)")
    print("=" * 70)
    print(f"Archivo: {ruta_archivo}")
    print(f"Usuario ejecutando: {github_user}\n")
    
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
        print("\n✓ Análisis sintáctico completado exitosamente")
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
    
    # Crear carpeta logs/ si no existe
    os.makedirs("logs", exist_ok=True)
    
    # Copiar parser.out a logs/ con el nombre correcto
    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f"logs/sintactico-{github_user}-{timestamp}.txt"
    
    # Buscar parser.out en varias ubicaciones posibles
    posibles_rutas = [
        "parser.out",
        "Lexer/parser.out",
        os.path.join(os.path.dirname(__file__), "parser.out")
    ]
    
    parser_out_encontrado = False
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            try:
                shutil.copy(ruta, log_filename)
                print(f"\n✓ Log guardado en: {log_filename}")
                parser_out_encontrado = True
                break
            except Exception as e:
                print(f"⚠️ Error al copiar desde {ruta}: {e}")
    
    if not parser_out_encontrado:
        print(f"\n⚠️ Advertencia: No se encontró parser.out")
        print(f"   Ubicaciones buscadas: {posibles_rutas}")
    
    print("=" * 70)


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    # Cambiar según quien ejecute
    GITHUB_USER = "TODOS"  # ← Cambiar aquí
    ARCHIVO_SWIFT = "Examples/pruebaGlobalSyntac.swift"
    
    analizar_archivo_swift(ARCHIVO_SWIFT, GITHUB_USER)