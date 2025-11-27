import ply.yacc as yacc
import os
import shutil
from datetime import datetime

# importar tokens del lexer global
from .analizador_lex import tokens, lexer

"""
ANALIZADOR SINTÁCTICO Y SEMÁNTICO GLOBAL - SWIFT
Proyecto de Lenguajes de Programación

INTEGRANTES:
1. Alexandre Icaza (aledicaz) - Regla 1 y 2
2. Alex Otero (alexoterol) - Regla 3 y 4
3. Jose Chong (Jlchong3) - Regla 5 y 6

ANÁLISIS SINTÁCTICO Y SEMÁNTICO COMPLETO DE SWIFT
"""


# <<< INICIO APORTE Alexandre Icaza
# estructuras para análisis semántico
class TablaSimbolos:
    """Tabla de símbolos con soporte para ámbitos anidados"""
    def __init__(self):
        self.ambitos = [{}]  # Lista de diccionarios (stack de ámbitos)

    def entrar_ambito(self):
        """Crear un nuevo ámbito"""
        self.ambitos.append({})

    def salir_ambito(self):
        """Salir del ámbito actual"""
        if len(self.ambitos) > 1:
            self.ambitos.pop()

    def agregar_simbolo(self, nombre, tipo, es_constante=False, tipo_retorno=None, linea=0):
        """Agregar símbolo al ámbito actual"""
        ambito_actual = self.ambitos[-1]
        ambito_actual[nombre] = {
            'tipo': tipo,
            'es_constante': es_constante,
            'tipo_retorno': tipo_retorno,  # Para funciones
            'linea': linea
        }

    def buscar_simbolo(self, nombre):
        """Buscar símbolo en todos los ámbitos (del más interno al más externo)"""
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None

    def existe_en_ambito_actual(self, nombre):
        """Verificar si el símbolo existe en el ámbito actual"""
        return nombre in self.ambitos[-1]

    def limpiar(self):
        self.ambitos = [{}]

# inicializar tabla de símbolos global
tabla_simbolos = TablaSimbolos()

# contexto para tracking de estructuras de control
contexto = {
    'en_bucle': 0,  # Contador de bucles anidados
    'en_funcion': False,  # Flag para saber si estamos dentro de una función
    'funcion_actual': None,  # Información de la función actual
    'errores_semanticos': []  # Lista de errores semánticos
}

def limpiar_contexto():
    """Reinicia el contexto global y los errores"""
    global contexto
    contexto['en_bucle'] = 0
    contexto['en_funcion'] = False
    contexto['funcion_actual'] = None
    contexto['errores_semanticos'] = []

def agregar_error_semantico(linea, columna, mensaje):
    """Agregar error semántico a la lista"""
    error = f"Error Semántico (Línea {linea}, Columna {columna}): {mensaje}"
    contexto['errores_semanticos'].append(error)
    print(f"❌ {error}")

def inferir_tipo(valor):
    """Inferir el tipo de un valor o expresión"""
    if valor is None:
        return None

    # Si es una tupla que representa un AST
    if isinstance(valor, tuple):
        tipo_nodo = valor[0]

        if tipo_nodo == 'literal':
            lit_val = valor[1]

            if isinstance(lit_val, bool):  # CORRECCIÓN: verificar bool antes de string
                return 'Bool'
            elif lit_val in ['true', 'false']:
                return 'Bool'
            elif isinstance(lit_val, int):
                return 'Int'
            elif isinstance(lit_val, float):
                return 'Double'
            elif isinstance(lit_val, str):
                return 'String'

            elif lit_val == 'nil':
                return 'Optional'

        elif tipo_nodo == 'identifier':
            nombre = valor[1]
            simbolo = tabla_simbolos.buscar_simbolo(nombre)
            if simbolo:
                return simbolo['tipo']
            return None

        elif tipo_nodo == 'binop':
            operador = valor[1]
            tipo_izq = inferir_tipo(valor[2])
            tipo_der = inferir_tipo(valor[3])

            # Operaciones aritméticas
            if operador in ['+', '-', '*', '/', '%']:
                if tipo_izq == tipo_der and tipo_izq in ['Int', 'Double']:
                    return tipo_izq
                # Permitir String + String
                if operador == '+' and tipo_izq == 'String' and tipo_der == 'String':
                    return 'String'
                return None  # Tipos incompatibles

        elif tipo_nodo == 'comparison':
            return 'Bool'

        elif tipo_nodo == 'logical':
            return 'Bool'

        elif tipo_nodo == 'array_literal':
            if len(valor[1]) > 0:
                tipo_primer_elem = inferir_tipo(valor[1][0])
                return ('array_type', tipo_primer_elem)
            return ('array_type', 'Any')

        elif tipo_nodo == 'function_call':
            nombre_func = valor[1]
            simbolo = tabla_simbolos.buscar_simbolo(nombre_func)
            if simbolo and simbolo.get('tipo_retorno'):
                return simbolo['tipo_retorno']
            return None

    return None

# precedencia de operadores
precedence = (
    ('right', 'QUESTION', 'COLON'),
    ('left', 'NIL_COALESCE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS', 'UPLUS', 'NOT'),
)

# reglas gramaticales
# regla inicial y estructura del programa
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

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
                 | break_statement
                 | continue_statement
                 | NEWLINE'''
    if p[1] != '\n':
        p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ('expr_stmt', p[1])


# <<< FIN APORTE Alexandre Icaza

# <<< INICIO APORTE Jose Chong

# declaración de variables (regla 6: redeclaración)
def p_variable_declaration(p):
    '''variable_declaration : LET IDENTIFIER COLON type_annotation ASSIGN expression
                           | VAR IDENTIFIER COLON type_annotation ASSIGN expression
                           | LET IDENTIFIER ASSIGN expression
                           | VAR IDENTIFIER ASSIGN expression
                           | LET IDENTIFIER COLON type_annotation
                           | VAR IDENTIFIER COLON type_annotation
                           | LET IDENTIFIER COLON tuple_type
                           | VAR IDENTIFIER COLON tuple_type'''

    nombre = p[2]
    linea = p.lineno(2)

    # REGLA 6: Verificar redeclaración en el mismo ámbito
    if tabla_simbolos.existe_en_ambito_actual(nombre):
        agregar_error_semantico(linea, 0,
            f"El identificador '{nombre}' ya ha sido declarado en este ámbito.")

    es_constante = (p[1] == 'let')

    if len(p) == 7:  # Con tipo y valor
        tipo_declarado = p[4]
        tipo_inferido = inferir_tipo(p[6])

        # Validar compatibilidad de tipos
        if tipo_inferido and tipo_declarado != tipo_inferido:
            if not (tipo_declarado == 'Double' and tipo_inferido == 'Int'):
                agregar_error_semantico(linea, 0,
                    f"Tipo incompatible: se esperaba '{tipo_declarado}' pero se asignó '{tipo_inferido}'.")

        tabla_simbolos.agregar_simbolo(nombre, tipo_declarado, es_constante, linea=linea)
        p[0] = ('var_decl', p[1], nombre, tipo_declarado, p[6])

    elif len(p) == 5 and p[3] == ':':  # Solo tipo
        tipo = p[4]
        tabla_simbolos.agregar_simbolo(nombre, tipo, es_constante, linea=linea)
        p[0] = ('var_decl', p[1], nombre, tipo, None)

    else:  # Sin tipo, con valor
        tipo_inferido = inferir_tipo(p[4])
        tabla_simbolos.agregar_simbolo(nombre, tipo_inferido, es_constante, linea=linea)
        p[0] = ('var_decl', p[1], nombre, tipo_inferido, p[4])

# <<< FIN APORTE Jose Chong

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

# arrays
def p_array_type(p):
    '''array_type : LBRACKET type_annotation RBRACKET'''
    p[0] = ('array_type', p[2])

def p_expression_array_literal(p):
    '''expression : LBRACKET array_elements RBRACKET
                  | LBRACKET RBRACKET'''
    if len(p) == 4:
        p[0] = ('array_literal', p[2])
    else:
        p[0] = ('array_literal', [])

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

# diccionarios
def p_dictionary_type(p):
    '''dictionary_type : LBRACKET type_annotation COLON type_annotation RBRACKET'''
    p[0] = ('dict_type', p[2], p[4])

def p_expression_dictionary_literal(p):
    '''expression : LBRACKET dictionary_pairs RBRACKET
                  | LBRACKET COLON RBRACKET'''
    if len(p) == 4 and p[2] == ':':
        p[0] = ('dict_literal', [])
    else:
        p[0] = ('dict_literal', p[2])

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

# tuplas
def p_tuple_type(p):
    '''tuple_type : LPAREN tuple_type_elements RPAREN'''
    p[0] = ('tuple_type', p[2])

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
    else:
        p[0] = p[1]

def p_expression_tuple_access(p):
    '''expression : expression DOT INT_LITERAL'''
    p[0] = ('tuple_access', p[1], p[3])

def p_expression_member_access(p):
    '''expression : expression DOT IDENTIFIER'''
    p[0] = ('member_access', p[1], p[3])

# <<< INICIO APORTE Alexandre Icaza

# asignación (regla 1: identificadores no declarados, regla 2: constantes)
def p_assignment(p):
    '''assignment : lvalue ASSIGN expression
                  | lvalue PLUS_ASSIGN expression
                  | lvalue MINUS_ASSIGN expression
                  | lvalue TIMES_ASSIGN expression
                  | lvalue DIV_ASSIGN expression
                  | lvalue MOD_ASSIGN expression'''

    lval = p[1]
    linea = p.lineno(2)

    # Extraer nombre del lvalue
    if lval[0] == 'identifier':
        nombre = lval[1]

        # REGLA 1: Verificar que el identificador esté declarado
        simbolo = tabla_simbolos.buscar_simbolo(nombre)
        if not simbolo:
            agregar_error_semantico(linea, 0,
                f"El identificador '{nombre}' no ha sido declarado en este ámbito.")
        else:
            # REGLA 2: Verificar que no sea una constante
            if simbolo['es_constante']:
                agregar_error_semantico(linea, 0,
                    f"Intento de modificar la constante '{nombre}', la cual no puede ser reasignada.")

            # REGLA 3: Verificar compatibilidad de tipos en operaciones compuestas
            if p[2] in ['+=', '-=', '*=', '/=', '%=']:
                tipo_var = simbolo['tipo']
                tipo_expr = inferir_tipo(p[3])

                if tipo_var and tipo_expr:
                    operador_base = p[2][0]  # Extraer +, -, *, /, %
                    if not validar_operacion_aritmetica(operador_base, tipo_var, tipo_expr, linea):
                        pass  # El error ya se agregó en validar_operacion_aritmetica

    p[0] = ('assignment', p[1], p[2], p[3])

def p_lvalue(p):
    '''lvalue : IDENTIFIER
              | SELF DOT IDENTIFIER
              | lvalue DOT IDENTIFIER
              | lvalue LBRACKET expression RBRACKET'''
    if len(p) == 2:
        p[0] = ('identifier', p[1])
    elif len(p) == 4 and p[2] == '.':
        if isinstance(p[1], str) and p[1] == 'self':
            p[0] = ('self_access', p[3])
        else:
            p[0] = ('member_access', p[1], p[3])
    else:
        p[0] = ('subscript_access', p[1], p[3])


# <<< FIN  APORTE Alexandre Icaza

# <<< INICIO APORTE Alex Otero

# expresiones aritméticas (regla 3: incompatibilidad de tipos)
def validar_operacion_aritmetica(operador, tipo1, tipo2, linea):
    """Validar compatibilidad de tipos en operaciones aritméticas"""
    tipos_numericos = ['Int', 'Double']

    # Permitir operaciones entre tipos numéricos
    if tipo1 in tipos_numericos and tipo2 in tipos_numericos:
        return True

    # Permitir + con String (concatenación)
    if operador == '+' and (tipo1 == 'String' or tipo2 == 'String'):
        return True

    # Operaciones no permitidas
    agregar_error_semantico(linea, 0,
        f"Operador '{operador}' no aplicable a los tipos '{tipo1}' y '{tipo2}'.")
    return False

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression'''

    operador = p[2]
    linea = p.lineno(2)

    # REGLA 3: Verificar compatibilidad de tipos
    tipo_izq = inferir_tipo(p[1])
    tipo_der = inferir_tipo(p[3])

    if tipo_izq and tipo_der:
        validar_operacion_aritmetica(operador, tipo_izq, tipo_der, linea)

    p[0] = ('binop', operador, p[1], p[3])

def p_expression_unary(p):
    '''expression : MINUS expression %prec UMINUS
                  | PLUS expression %prec UPLUS'''
    p[0] = ('unary', p[1], p[2])

# expresiones lógicas y booleanas

def p_expression_logical(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = ('logical', p[2], p[1], p[3])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = ('not', p[2])

def p_expression_comparison(p):
    '''expression : expression EQ expression
                  | expression NE expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression'''
    p[0] = ('comparison', p[2], p[1], p[3])

# operador ternario y nil-coalescing
def p_expression_ternary(p):
    '''expression : expression QUESTION expression COLON expression'''
    p[0] = ('ternary', p[1], p[3], p[5])

def p_expression_nil_coalescing(p):
    '''expression : expression NIL_COALESCE expression'''
    p[0] = ('nil_coalesce', p[1], p[3])

# expresiones básicas y literales (regla 1: uso de identificadores)

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
    # CORRECCIÓN: Convertir true/false a booleanos Python
    if p[1] == 'true':
        p[0] = ('literal', True)
    elif p[1] == 'false':
        p[0] = ('literal', False)
    else:
        p[0] = ('literal', p[1])

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    nombre = p[1]
    linea = p.lineno(1)

    # REGLA 1: Verificar que el identificador esté declarado
    simbolo = tabla_simbolos.buscar_simbolo(nombre)
    if not simbolo:
        agregar_error_semantico(linea, 0,
            f"El identificador '{nombre}' no ha sido declarado en este ámbito.")

    p[0] = ('identifier', nombre)

def p_expression_self_access(p):
    '''expression : SELF DOT IDENTIFIER'''
    p[0] = ('self_access', p[3])

# llamadas a función como expresión
def p_expression_function_call(p):
    '''expression : IDENTIFIER LPAREN argument_list RPAREN
                  | IDENTIFIER LPAREN RPAREN'''
    function_name = p[1]
    linea = p.lineno(1)

    # REGLA 1: Verificar que la función esté declarada
    simbolo = tabla_simbolos.buscar_simbolo(function_name)
    if not simbolo:
        # Permitir funciones built-in como print, readLine
        if function_name not in ['print', 'readLine']:
            agregar_error_semantico(linea, 0,
                f"El identificador '{function_name}' no ha sido declarado en este ámbito.")

    if len(p) == 5:
        arguments = p[3]
        p[0] = ('function_call', function_name, arguments)
    else:
        p[0] = ('function_call', function_name, [])

# estructuras de control: for-in (regla 4: contexto de bucle)

def p_for_statement(p):
    '''for_statement : for_header LBRACE statement_list RBRACE'''

    header_info = p[1]
    nombre_var = header_info['nombre_var']
    rango = header_info['rango']

    # Salir del bucle
    contexto['en_bucle'] -= 1

    # Salir del ámbito
    tabla_simbolos.salir_ambito()

    p[0] = ('for_in', nombre_var, rango, p[3])

def p_for_header(p):
    '''for_header : FOR IDENTIFIER IN range_expression
                  | FOR IDENTIFIER IN expression'''

    nombre_var = p[2]
    linea = p.lineno(2)
    rango = p[4]

    # CRÍTICO: Entrar en nuevo ámbito ANTES de procesar el cuerpo
    tabla_simbolos.entrar_ambito()

    # Declarar variable de iteración
    tabla_simbolos.agregar_simbolo(nombre_var, 'Int', False, linea=linea)

    # Marcar que estamos en un bucle
    contexto['en_bucle'] += 1

    p[0] = {
        'nombre_var': nombre_var,
        'rango': rango
    }

def p_range_expression(p):
    '''range_expression : expression CLOSED_RANGE expression
                        | expression HALF_OPEN_RANGE expression'''
    p[0] = ('range', p[2], p[1], p[3])

# estructura de control: if-else
def p_if_statement(p):
    '''if_statement : IF expression LBRACE statement_list RBRACE
                    | IF expression LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
                    | IF expression LBRACE statement_list RBRACE else_if_chain
                    | IF expression LBRACE statement_list RBRACE else_if_chain ELSE LBRACE statement_list RBRACE'''

    if len(p) == 6:
        p[0] = ('if', p[2], p[4], None, None)
    elif len(p) == 10 and p[6] == 'else':
        p[0] = ('if_else', p[2], p[4], p[8])
    elif len(p) == 7:
        p[0] = ('if_elif', p[2], p[4], p[6], None)
    else:
        p[0] = ('if_elif_else', p[2], p[4], p[6], p[9])

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

# estructura de control: guard
def p_guard_statement(p):
    '''guard_statement : GUARD expression ELSE LBRACE statement_list RBRACE'''
    p[0] = ('guard', p[2], p[5])

# estructura de control: while (regla 4: contexto de bucle)
def p_while_statement(p):
    '''while_statement : while_header LBRACE statement_list RBRACE'''

    condicion = p[1]

    # Salir del bucle
    contexto['en_bucle'] -= 1

    p[0] = ('while', condicion, p[3])

def p_while_header(p):
    '''while_header : WHILE expression'''

    # CRÍTICO: Marcar que estamos en un bucle ANTES de procesar el cuerpo
    contexto['en_bucle'] += 1

    p[0] = p[2]

# break y continue (regla 4: fuera de bucle)

def p_break_statement(p):
    '''break_statement : BREAK'''
    linea = p.lineno(1)

    # REGLA: Verificar que estemos dentro de un bucle
    if contexto['en_bucle'] == 0:
        agregar_error_semantico(linea, 0, "La sentencia 'break' solo puede aparecer dentro de un bucle.")

    p[0] = ('break',)

def p_continue_statement(p):
    '''continue_statement : CONTINUE'''
    if p[1] == 'continue':
        linea = p.lineno(1)

        # REGLA 4: Verificar que estemos dentro de un bucle
        if contexto['en_bucle'] == 0:
            agregar_error_semantico(linea, 0,
                "La sentencia 'continue' solo puede aparecer dentro de un bucle.")

        p[0] = ('continue',)

# estructura de control: switch-case

def p_switch_statement(p):
    '''switch_statement : SWITCH expression LBRACE optional_newlines case_list optional_newlines RBRACE
                        | SWITCH expression LBRACE optional_newlines case_list default_case optional_newlines RBRACE'''
    if len(p) == 9:
        p[0] = ('switch', p[2], p[5], p[6])
    else:
        p[0] = ('switch', p[2], p[5], None)

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

def p_optional_newlines(p):
    '''optional_newlines : optional_newlines NEWLINE
                         | empty'''
    pass


# <<< FIN APORTE Alex Otero

# <<< INICIO APORTE Jose Chong

# funciones (regla 5: tipo de retorno)
# nueva regla intermedia para manejar el inicio de función
def p_function_declaration(p):
    '''function_declaration : func_header LBRACE statement_list RBRACE'''

    header_info = p[1]
    nombre_func = header_info['nombre']
    parametros = header_info['parametros']
    tipo_retorno = header_info['tipo_retorno']
    cuerpo = p[3]

    # Restaurar contexto
    contexto['funcion_actual'] = header_info['contexto_previo']
    contexto['en_funcion'] = (header_info['contexto_previo'] is not None)

    # Salir del ámbito de la función
    tabla_simbolos.salir_ambito()

    if tipo_retorno:
        p[0] = ('func_decl', nombre_func, parametros, tipo_retorno, cuerpo)
    else:
        p[0] = ('func_decl', nombre_func, parametros, None, cuerpo)


def p_func_header(p):
    '''func_header : FUNC IDENTIFIER LPAREN parameter_list RPAREN ARROW type_annotation
                   | FUNC IDENTIFIER LPAREN RPAREN ARROW type_annotation
                   | FUNC IDENTIFIER LPAREN parameter_list RPAREN
                   | FUNC IDENTIFIER LPAREN RPAREN'''

    nombre_func = p[2]
    linea = p.lineno(2)

    # REGLA 6: Verificar redeclaración
    if tabla_simbolos.existe_en_ambito_actual(nombre_func):
        agregar_error_semantico(linea, 0,
            f"El identificador '{nombre_func}' ya ha sido declarado en este ámbito.")

    # Determinar parámetros y tipo de retorno
    if len(p) == 8:  # Con parámetros y tipo de retorno
        parametros = p[4]
        tipo_retorno = p[7]
    elif len(p) == 7:  # Sin parámetros, con tipo de retorno
        parametros = []
        tipo_retorno = p[6]
    elif len(p) == 6:  # Con parámetros, sin tipo de retorno
        parametros = p[4]
        tipo_retorno = None
    else:  # Sin parámetros, sin tipo de retorno
        parametros = []
        tipo_retorno = None

    # Agregar función a la tabla de símbolos GLOBAL
    tabla_simbolos.agregar_simbolo(nombre_func, 'Function', False, tipo_retorno, linea)

    # CRÍTICO: Entrar en nuevo ámbito ANTES de procesar el cuerpo
    tabla_simbolos.entrar_ambito()

    # Guardar contexto de función actual ANTES de procesar el cuerpo
    contexto_previo = contexto['funcion_actual']
    contexto['en_funcion'] = True
    contexto['funcion_actual'] = {
        'nombre': nombre_func,
        'tipo_retorno': tipo_retorno
    }

    # CRÍTICO: Agregar parámetros al ámbito ANTES de procesar el cuerpo
    for param in parametros:
        if param[0] == 'param':
            nombre_param = param[1]
            tipo_param = param[2]
            tabla_simbolos.agregar_simbolo(nombre_param, tipo_param, False)
        elif param[0] == 'param_default':
            nombre_param = param[1]
            tipo_param = param[2]
            tabla_simbolos.agregar_simbolo(nombre_param, tipo_param, False)

    # Retornar información del header para usarla después
    p[0] = {
        'nombre': nombre_func,
        'parametros': parametros,
        'tipo_retorno': tipo_retorno,
        'contexto_previo': contexto_previo
    }

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

# return (regla 5: tipo de retorno de función)
def p_return_statement(p):
    '''return_statement : RETURN expression
                        | RETURN'''

    linea = p.lineno(1)

    # CORRECCIÓN: Verificar que estemos dentro de una función
    if not contexto['en_funcion']:
        agregar_error_semantico(linea, 0,
            "La sentencia 'return' solo puede aparecer dentro de una función.")
        p[0] = ('return', p[2] if len(p) == 3 else None)
        return

    # REGLA 5: Verificar tipo de retorno
    if contexto['funcion_actual']:
        tipo_retorno_esperado = contexto['funcion_actual']['tipo_retorno']
        nombre_funcion = contexto['funcion_actual']['nombre']

        if len(p) == 3:  # return con valor
            tipo_retornado = inferir_tipo(p[2])

            if tipo_retorno_esperado is None:
                agregar_error_semantico(linea, 0,
                    f"La función '{nombre_funcion}' no debe retornar ningún valor.")
            elif tipo_retornado and tipo_retorno_esperado != tipo_retornado:
                # Permitir Int -> Double
                if not (tipo_retorno_esperado == 'Double' and tipo_retornado == 'Int'):
                    agregar_error_semantico(linea, 0,
                        f"La función '{nombre_funcion}' debe retornar un valor de tipo '{tipo_retorno_esperado}', pero se está retornando un valor de tipo '{tipo_retornado}'.")

            p[0] = ('return', p[2])
        else:  # return sin valor
            if tipo_retorno_esperado is not None:
                agregar_error_semantico(linea, 0,
                    f"La función '{nombre_funcion}' debe retornar un valor de tipo '{tipo_retorno_esperado}'.")

            p[0] = ('return', None)

# <<< FIN APORTE Jose Chong

# entrada/salida: print y readline
def p_function_call_statement(p):
    '''function_call_statement : IDENTIFIER LPAREN argument_list RPAREN
                               | IDENTIFIER LPAREN RPAREN'''
    function_name = p[1]
    linea = p.lineno(1)

    if len(p) == 5:
        arguments = p[3]
        if function_name == 'print':
            p[0] = ('print', arguments)
        elif function_name == 'readLine':
            if len(arguments) <= 1:
                p[0] = ('readline', arguments[0] if arguments else None)
            else:
                print(f"❌ Error: readLine() solo acepta 0 o 1 argumento(s)")
                p[0] = ('error', 'readLine con argumentos incorrectos')
        else:
            # REGLA 1: Verificar que la función esté declarada
            simbolo = tabla_simbolos.buscar_simbolo(function_name)
            if not simbolo:
                agregar_error_semantico(linea, 0,
                    f"El identificador '{function_name}' no ha sido declarado en este ámbito.")

            p[0] = ('function_call', function_name, arguments)
    else:
        if function_name == 'print':
            p[0] = ('print', [])
        elif function_name == 'readLine':
            p[0] = ('readline', None)
        else:
            simbolo = tabla_simbolos.buscar_simbolo(function_name)
            if not simbolo:
                agregar_error_semantico(linea, 0,
                    f"El identificador '{function_name}' no ha sido declarado en este ámbito.")

            p[0] = ('function_call', function_name, [])

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# poo: clases
def p_class_declaration(p):
    '''class_declaration : class_header LBRACE class_body RBRACE'''

    nombre_clase = p[1]

    # Salir del ámbito de la clase
    tabla_simbolos.salir_ambito()

    p[0] = ('class_decl', nombre_clase, p[3])

def p_class_header(p):
    '''class_header : CLASS IDENTIFIER'''

    nombre_clase = p[2]
    linea = p.lineno(2)

    # REGLA 6: Verificar redeclaración
    if tabla_simbolos.existe_en_ambito_actual(nombre_clase):
        agregar_error_semantico(linea, 0,
            f"El identificador '{nombre_clase}' ya ha sido declarado en este ámbito.")

    # Agregar clase a la tabla de símbolos
    tabla_simbolos.agregar_simbolo(nombre_clase, 'Class', False, linea=linea)

    # CRÍTICO: Entrar en ámbito de clase ANTES de procesar el cuerpo
    tabla_simbolos.entrar_ambito()

    p[0] = nombre_clase

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

def p_computed_property(p):
    '''computed_property : VAR IDENTIFIER COLON type_annotation LBRACE optional_newlines GET LBRACE optional_newlines statement_list optional_newlines RBRACE optional_newlines RBRACE'''
    p[0] = ('computed_property', p[2], p[4], p[10])

def p_init_declaration(p):
    '''init_declaration : init_header LBRACE statement_list RBRACE'''

    header_info = p[1]
    parametros = header_info['parametros']

    # Restaurar contexto
    contexto['en_funcion'] = False

    # Salir del ámbito del init
    tabla_simbolos.salir_ambito()

    p[0] = ('init', parametros, p[3])

def p_init_header(p):
    '''init_header : INIT LPAREN parameter_list RPAREN
                   | INIT LPAREN RPAREN'''

    if len(p) == 5:
        parametros = p[3]
    else:
        parametros = []

    # CRÍTICO: Entrar en ámbito ANTES de procesar el cuerpo
    tabla_simbolos.entrar_ambito()
    contexto['en_funcion'] = True

    # Agregar parámetros al ámbito
    for param in parametros:
        if param[0] == 'param':
            nombre_param = param[1]
            tipo_param = param[2]
            tabla_simbolos.agregar_simbolo(nombre_param, tipo_param, False)
        elif param[0] == 'param_default':
            nombre_param = param[1]
            tipo_param = param[2]
            tabla_simbolos.agregar_simbolo(nombre_param, tipo_param, False)

    p[0] = {'parametros': parametros}

def p_method_declaration(p):
    '''method_declaration : method_header LBRACE statement_list RBRACE'''

    header_info = p[1]
    nombre = header_info['nombre']
    parametros = header_info['parametros']
    tipo_retorno = header_info['tipo_retorno']

    # Restaurar contexto
    contexto['funcion_actual'] = None
    contexto['en_funcion'] = False

    # Salir del ámbito del método
    tabla_simbolos.salir_ambito()

    if tipo_retorno:
        p[0] = ('method', nombre, parametros, tipo_retorno, p[3])
    else:
        p[0] = ('method', nombre, parametros, None, p[3])

def p_method_header(p):
    '''method_header : FUNC IDENTIFIER LPAREN parameter_list RPAREN ARROW type_annotation
                     | FUNC IDENTIFIER LPAREN RPAREN ARROW type_annotation
                     | FUNC IDENTIFIER LPAREN parameter_list RPAREN
                     | FUNC IDENTIFIER LPAREN RPAREN'''

    nombre = p[2]

    # Determinar parámetros y tipo de retorno
    if len(p) == 8:  # Con parámetros y tipo de retorno
        parametros = p[4]
        tipo_retorno = p[7]
    elif len(p) == 7:  # Sin parámetros, con tipo de retorno
        parametros = []
        tipo_retorno = p[6]
    elif len(p) == 6:  # Con parámetros, sin tipo de retorno
        parametros = p[4]
        tipo_retorno = None
    else:  # Sin parámetros, sin tipo de retorno
        parametros = []
        tipo_retorno = None

    # CRÍTICO: Entrar en ámbito ANTES de procesar el cuerpo
    tabla_simbolos.entrar_ambito()
    contexto['en_funcion'] = True
    contexto['funcion_actual'] = {
        'nombre': nombre,
        'tipo_retorno': tipo_retorno
    }

    # Agregar parámetros al ámbito
    for param in parametros:
        if param[0] == 'param':
            nombre_param = param[1]
            tipo_param = param[2]
            tabla_simbolos.agregar_simbolo(nombre_param, tipo_param, False)
        elif param[0] == 'param_default':
            nombre_param = param[1]
            tipo_param = param[2]
            tabla_simbolos.agregar_simbolo(nombre_param, tipo_param, False)

    p[0] = {
        'nombre': nombre,
        'parametros': parametros,
        'tipo_retorno': tipo_retorno
    }

# auxiliares
def p_empty(p):
    '''empty :'''
    pass

# manejo de errores
def p_error(p):
    if p:
        value = '\\n' if p.value == '\n' else p.value
        error_msg = f"Error de sintaxis en línea {p.lineno}: Token inesperado '{value}' (tipo: {p.type})"
        print(f"❌ {error_msg}")
    else:
        error_msg = "Error de sintaxis: Final de archivo inesperado"
        print(f"❌ {error_msg}")

# construcción del parser
parser = yacc.yacc()

# funciones de análisis y generación de logs
def generar_log_semantico(github_user):
    """Genera el contenido del log semántico"""
    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")

    log_lines = []
    log_lines.append("=" * 70)
    log_lines.append("ANÁLISIS SEMÁNTICO - SWIFT")
    log_lines.append("=" * 70)
    log_lines.append(f"Usuario: {github_user}")
    log_lines.append(f"Fecha y hora: {timestamp}")
    log_lines.append("=" * 70)
    log_lines.append("")

    if len(contexto['errores_semanticos']) != 0:
        log_lines.append(f"Total de errores semánticos: {len(contexto['errores_semanticos'])}")
        log_lines.append("")
        for i, error in enumerate(contexto['errores_semanticos'], 1):
            log_lines.append(f"{i}. {error}")

    log_lines.append("")
    log_lines.append("=" * 70)
    log_lines.append("REGLAS SEMÁNTICAS IMPLEMENTADAS:")
    log_lines.append("=" * 70)
    log_lines.append("1. Uso de Identificadores No Declarados")
    log_lines.append("   - Verifica que variables y funciones estén declaradas antes de usarse")
    log_lines.append("")
    log_lines.append("2. Asignación a una Constante")
    log_lines.append("   - Impide modificar variables declaradas con 'let'")
    log_lines.append("")
    log_lines.append("3. Incompatibilidad de Tipos en Operaciones Aritméticas")
    log_lines.append("   - Valida compatibilidad de tipos en operaciones (+, -, *, /, %)")
    log_lines.append("")
    log_lines.append("4. Sentencia break o continue Fuera de un Bucle")
    log_lines.append("   - Verifica que break/continue solo aparezcan dentro de bucles")
    log_lines.append("")
    log_lines.append("5. Tipo de Retorno de Función Incorrecto")
    log_lines.append("   - Valida que el tipo retornado coincida con la declaración")
    log_lines.append("")
    log_lines.append("6. Redeclaración de Variable en el Mismo Ámbito")
    log_lines.append("   - Impide declarar dos veces el mismo identificador en un ámbito")
    log_lines.append("=" * 70)

    return "\n".join(log_lines)

def analizar_archivo_swift(ruta_archivo: str, github_user: str):
    """
    Lee un archivo Swift, lo analiza sintáctica y semánticamente,
    y genera logs de ambos análisis
    """
    print("=" * 70)
    print("ANALIZADOR SINTÁCTICO Y SEMÁNTICO GLOBAL DE SWIFT")
    print("Proyecto de Lenguajes de Programación")
    print("=" * 70)
    print("Integrantes:")
    print("  - Alexandre Icaza (aledicaz)")
    print("  - Alex Otero (alexoterol)")
    print("  - Jose Chong (Jlchong3)")
    print("=" * 70)
    print(f"Archivo: {ruta_archivo}")
    print(f"Usuario ejecutando: {github_user}\n")

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{ruta_archivo}'")
        return
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return

    # Reiniciar estructuras semánticas
    global tabla_simbolos, contexto
    tabla_simbolos = TablaSimbolos()
    contexto = {
        'en_bucle': 0,
        'en_funcion': False,
        'funcion_actual': None,
        'errores_semanticos': []
    }

    print("Analizando sintaxis y semántica...\n")
    try:
        result = parser.parse(codigo, lexer=lexer)

        if len(contexto['errores_semanticos']) != 0:
            print(f"\n❌ Se encontraron {len(contexto['errores_semanticos'])} errores semánticos")

    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")

    # Crear carpeta logs si no existe
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")

    # Guardar log sintáctico (parser.out)
    log_sintactico = f"logs/sintactico-{github_user}-{timestamp}.txt"
    posibles_rutas = [
        "parser.out",
        "Lexers_Individuales/parser.out",
        os.path.join(os.path.dirname(__file__), "parser.out")
    ]

    parser_out_encontrado = False
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            try:
                shutil.copy(ruta, log_sintactico)
                parser_out_encontrado = True
                break
            except Exception as e:
                print(f"⚠️ Error al copiar desde {ruta}: {e}")

    if not parser_out_encontrado:
        print(f"\n⚠️ Advertencia: No se encontró parser.out")
        print(f"   Ubicaciones buscadas: {posibles_rutas}")

    # Guardar log semántico
    log_semantico = f"logs/semantico-{github_user}-{timestamp}.txt"
    contenido_log = generar_log_semantico(github_user)

    try:
        with open(log_semantico, "w", encoding="utf-8") as f:
            f.write(contenido_log)
    except Exception as e:
        print(f"❌ Error al guardar log semántico: {e}")

    print("=" * 70)
    print(f"\nRESUMEN DEL ANÁLISIS:")
    print(f"  - Errores semánticos encontrados: {len(contexto['errores_semanticos'])}")
    print("=" * 70)


# main
if __name__ == "__main__":
    GITHUB_USER = "Alex Otero"
    ARCHIVO_SWIFT = "Examples/pruebaSemanticaGlobal.swift"

    analizar_archivo_swift(ARCHIVO_SWIFT, GITHUB_USER)
