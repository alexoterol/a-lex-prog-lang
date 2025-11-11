import ply.yacc as yacc
import os
import shutil
from datetime import datetime

# Importar tokens del lexer global
from analizador_lex import tokens, lexer

# <<< INICIO APORTE Jose Chong

"""
ANALIZADOR SINTÁCTICO - SWIFT
Integrante: Jose Chong (Jlchong3)

Responsabilidades:
1. Entrada/Salida: print() con interpolación de strings, readLine()
2. Programación Orientada a Objetos: clases, propiedades, inicializadores, métodos
3. Estructura de Datos: Tuplas
4. Estructura de Control: Switch-case
5. Funciones: Métodos de clase con self
"""

# PRECEDENCIA DE OPERADORES
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
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
    '''statement : function_call_statement
                 | class_declaration
                 | switch_statement
                 | variable_declaration
                 | expression
                 | return_statement
                 | NEWLINE'''
    if p[1] != '\n':
        p[0] = p[1]


# ENTRADA/SALIDA - PRINT y READLINE
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
            if len(arguments) == 1:
                p[0] = ('readline', arguments[0])
                print("✓ Lectura de entrada: readLine(con 1 argumento)")
            else:
                print(f"❌ Error sintáctico: readLine() solo acepta 0 o 1 argumento(s). Se encontraron {len(arguments)}. Línea {p.lineno(1)}")
                p[0] = ('error', 'readLine con argumentos incorrectos')

        else:
            p[0] = ('function_call', function_name, arguments)

    else:
        if function_name == 'print':
            p[0] = ('print', [])
            print("✓ Print vacío")

        elif function_name == 'readLine':
            p[0] = ('readline', None)
            print("✓ Lectura de entrada: readLine()")

        else:
            p[0] = ('function_call', function_name, [])


def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# POO - DECLARACIÓN DE CLASES
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


# POO - PROPIEDADES ALMACENADAS
def p_property_declaration(p):
    '''property_declaration : VAR IDENTIFIER COLON type_annotation
                           | LET IDENTIFIER COLON type_annotation
                           | VAR IDENTIFIER COLON tuple_type
                           | LET IDENTIFIER COLON tuple_type'''
    p[0] = ('property', p[1], p[2], p[4])
    print(f"✓ Propiedad: {p[1]} {p[2]}: {p[4]}")


# POO - PROPIEDADES COMPUTADAS
def p_computed_property(p):
    '''computed_property : VAR IDENTIFIER COLON type_annotation LBRACE optional_newlines GET LBRACE optional_newlines statement_list optional_newlines RBRACE optional_newlines RBRACE'''
    p[0] = ('computed_property', p[2], p[4], p[10])
    print(f"✓ Propiedad computada: var {p[2]}: {p[4]}")


# POO - INICIALIZADORES
def p_init_declaration(p):
    '''init_declaration : INIT LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                        | INIT LPAREN RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 8:
        p[0] = ('init', p[3], p[6])
        print(f"✓ Inicializador: init({len(p[3])} parámetros)")
    else:
        p[0] = ('init', [], p[5])
        print("✓ Inicializador: init()")


# POO - MÉTODOS DE INSTANCIA
def p_method_declaration(p):
    '''method_declaration : FUNC IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
                          | FUNC IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACE'''
    if len(p) == 9:
        p[0] = ('method', p[2], p[4], p[7])
        print(f"✓ Método: func {p[2]}({len(p[4])} parámetros)")
    else:
        p[0] = ('method', p[2], [], p[6])
        print(f"✓ Método: func {p[2]}()")


# POO - ACCESO CON SELF
def p_expression_self_access(p):
    '''expression : SELF DOT IDENTIFIER'''
    p[0] = ('self_access', p[3])
    print(f"✓ Acceso a propiedad: self.{p[3]}")


# TUPLAS - DECLARACIÓN
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


# TUPLAS - ACCESO
def p_expression_tuple_access(p):
    '''expression : expression DOT INT_LITERAL'''
    p[0] = ('tuple_access', p[1], p[3])
    print(f"✓ Acceso a tupla por índice: .{p[3]}")

def p_expression_tuple_named_access(p):
    '''expression : expression DOT IDENTIFIER'''
    # Diferenciamos si es acceso a tupla nombrada o propiedad
    p[0] = ('member_access', p[1], p[3])
    print(f"✓ Acceso: .{p[3]}")


# SWITCH-CASE
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


# EXPRESIONES BÁSICAS
def p_variable_declaration(p):
    '''variable_declaration : LET IDENTIFIER COLON type_annotation
                           | VAR IDENTIFIER COLON type_annotation
                           | LET IDENTIFIER COLON tuple_type
                           | VAR IDENTIFIER COLON tuple_type'''
    p[0] = ('var_decl', p[1], p[2], p[4])
    print(f"✓ Declaración: {p[1]} {p[2]}: {p[4]}")

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

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


# AUXILIARES
def p_return_statement(p):
    '''return_statement : RETURN expression
                        | RETURN'''
    if len(p) == 3:
        p[0] = ('return', p[2])
        print("✓ Return con valor")
    else:
        p[0] = ('return', None)
        print("✓ Return")

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

def p_type_annotation(p):
    '''type_annotation : TYPE_INT
                       | TYPE_DOUBLE
                       | TYPE_BOOL
                       | TYPE_STRING
                       | IDENTIFIER'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_optional_newlines(p):
    '''optional_newlines : optional_newlines NEWLINE
                         | empty'''
    pass



# MANEJO DE ERRORES
def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en línea {p.lineno}: Token inesperado '{p.value}' (tipo: {p.type})"
        print(f"❌ {error_msg}")
    else:
        error_msg = "Error de sintaxis: Final de archivo inesperado"
        print(f"❌ {error_msg}")


# CONSTRUCCIÓN DEL PARSER
parser = yacc.yacc(debug=True, outputdir=os.path.dirname(__file__) or '.')


# FUNCIÓN PARA ANALIZAR ARCHIVO
def analizar_archivo_swift(ruta_archivo: str, github_user: str):
    """
    Lee un archivo Swift, lo analiza y copia el parser.out a logs/
    """
    print("=" * 70)
    print("ANALIZADOR SINTÁCTICO DE SWIFT - Entrada/Salida y POO")
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

    # Copiar parser.out a logs/
    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f"logs/sintactico-{github_user}-{timestamp}.txt"

    # Buscar parser.out en varias ubicaciones posibles
    posibles_rutas = [
        "parser.out",
        "Lexers_Individuales/parser.out",
        os.path.join(os.path.dirname(__file__), "parser.out")
    ]

    parser_out_encontrado = False
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            print(f"\n✓ parser.out encontrado en: {ruta}")
            try:
                shutil.copy(ruta, log_filename)
                print(f"✓ Log guardado en: {log_filename}")
                parser_out_encontrado = True
                break
            except Exception as e:
                print(f"❌ Error al copiar desde {ruta}: {e}")

    if not parser_out_encontrado:
        print(f"\n⚠️  Advertencia: No se encontró parser.out en ninguna ubicación")
        print(f"   Buscado en: {posibles_rutas}")

    print("=" * 70)


if __name__ == "__main__":
    GITHUB_USER = "Jlchong3"
    ARCHIVO_SWIFT = "Examples/josechong_prueba_sintactico.swift"

    analizar_archivo_swift(ARCHIVO_SWIFT, GITHUB_USER)

# <<< FIN APORTE Jose Chong
