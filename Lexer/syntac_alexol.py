"""
🟩 Integrante 2 - Control de Flujo y Lógica
Responsabilidades:

Condiciones y Lógica:

Expresiones booleanas                   DONE
Operadores lógicos (&&, ||, !)          DONE
Condiciones con múltiples conectores    DONE
Operador ternario (? :)                 DONE
Nil-coalescing (??)                     DONE


Estructura de Control (obligatoria):

Condicionales if-else                   DONE
if-else if-else                         
guard statements                        


Estructura de Datos (obligatoria):

Diccionarios [String: Int], [String: Any], etc.     
Declaración e inicialización de diccionarios        
Acceso a valores por clave                          


Estructura de Control adicional:

Bucle while                             
Condiciones de bucle                    


Función (obligatoria):

Funciones con parámetros opcionales                 
Funciones con valores por defecto                       
Sintaxis: func nombre(param: Type? = nil) -> Type { }   
"""

import ply.yacc as yacc
from analizador_lex import tokens

def p__sentences(p):
    '''sentences : bool_exp
                | assign
                | expression
                |
    '''

def p_bool_exp(p):
    '''bool_exp : value
                | value bool_operator bool_exp
    '''

def p_assign(p):
    '''assign : type_data IDENTIFIER ASSIGN value'''

def p_expression_ternary(p):
    '''expression : bool_exp QUESTION value COLON value
    '''

def p_expression_nil_coalescing(p):
    '''expression : IDENTIFIER NIL_COALESCE STRING'''

# def p_program_statements(p):
#     '''program : statement
#                 | program statement'''

# def p_block(p):
#     '''block : LBRACE program RBRACE
#              | LBRACE RBRACE'''

# def p_statement_if(p):
#     '''statement : IF expression block
#                  | IF expression block ELSE statement'''

# def p_statement_return(p):
#     'statement : RETURN'

# def p_statement_guard(p):
#     'statement : GUARD expression ELSE block'

def p_bool_operator(p):
    '''bool_operator : AND
                    | OR
    '''

def p_bool_neg(p):
    '''bool_neg : NOT'''



def p_type_data(p):
    '''type_data : VAR
                | LET
    '''

def p_value(p):
    '''value : INT_LITERAL
             | FLOAT_LITERAL
             | IDENTIFIER
             | STRING
             | NIL'''

def p_bool_value(p):
    '''value : TRUE
            | FALSE
            | bool_neg value
    '''

# # Definición de Precedencia y Asociatividad (de menor a mayor)
# precedence = (
#     # 1. Lógica (Menor Precedencia)
#     ('left', 'OR'),       # ||
#     ('left', 'AND'),      # &&

#     # 2. Nil-Coalescing (Asociatividad Derecha)
#     ('right', 'DOUBLQMARK'), # ??

#     # 3. Ternario Condicional (Asociatividad Derecha)
#     # Nota: El operador ternario no es asociativo en Swift,
#     # pero definirlo como 'right' en yacc funciona bien para su parsing.
#     ('right', 'QMARK', 'COLON'), # ? :

#     # 4. Comparación (Non-associative, no se encadenan como 1 < 2 < 3)
#     ('nonassoc', 'EQ', 'NE'),
#     ('nonassoc', 'LT', 'LE', 'GT', 'GE'),

#     # 5. Unario (Mayor Precedencia)
#     ('right', 'NOT')      # !
# )

# def p_expression_nil_coalescing(p):
#     'expression : expression NIL_COALESCE expression'
#     # Ejemplo: optionalValue ?? defaultValue
#     p[0] = ('nil_coalescing', p[1], p[3])


# def p_expression_ternary(p):
#     'expression : expression QUESTION expression COLON expression'
#     # p[1]: Condición (debe ser booleana)
#     # p[3]: Expresión si verdadero
#     # p[5]: Expresión si falso
#     p[0] = ('ternary', p[1], p[3], p[5])


# def p_expression_binary_logical(p):
#     '''expression : expression AND expression
#                   | expression OR expression'''
#     p[0] = ('binary_logical_op', p[2], p[1], p[3])

# def p_expression_unary_not(p):
#     'expression : NOT expression'
#     p[0] = ('unary_logical_op', p[1], p[2])

# def p_expression_literal_value(p):
#     '''expression : TRUE
#                   | FALSE
#                   | IDENTIFIER
#                   | INT_LITERAL
#                   | FLOAT_LITERAL'''
#     p[0] = p[1]

# # 1. El programa es una lista de declaraciones (statements)
# def p_program(p):
#     '''program : statement
#                | program statement'''
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[1].append(p[2])
#         p[0] = p[1]

# # 2. Bloque de Código (rodeado de llaves)
# def p_block(p):
#     '''block : LBRACE program RBRACE
#              | LBRACE RBRACE''' # Bloque vacío
#     p[0] = p[2] if len(p) == 4 else []

# # 3. La regla base para IF
# def p_statement_if(p):
#     '''statement : IF expression block
#                  | IF expression block ELSE statement'''
#     # IF expression block
#     if len(p) == 4:
#         p[0] = ('if', p[2], p[3], None)
#     # IF expression block ELSE statement (donde el statement puede ser otro IF)
#     elif len(p) == 6:
#         p[0] = ('if', p[2], p[3], p[5])
    
# def p_statement_guard(p):
#     'statement : GUARD expression ELSE LBRACE statement_list RBRACE'
#     # Nota: Aquí he asumido 'statement_list' para permitir múltiples
#     # instrucciones dentro del else, pero solo una simple 'RETURN'
#     # o 'THROW' es suficiente para cumplir el requisito mínimo de Swift.
#     p[0] = ('guard', p[2], p[5])

# # Regla simple para la lista de declaraciones dentro del guard/bloque
# def p_statement_list(p):
#     '''statement_list : statement
#                       | statement_list statement'''
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[1].append(p[2])
#         p[0] = p[1]

# # Una instrucción de transferencia de control simple
# def p_statement_return(p):
#     'statement : RETURN'
#     p[0] = ('return',)



# Error rule for syntax errors
def p_error(p):
    # Asegúrate de imprimir un error más informativo
    if p:
        print(f"Syntax error at token '{p.value}' in line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()


while True:
   try:
       s = input('Swift > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)