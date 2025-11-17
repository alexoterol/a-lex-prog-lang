// ============================================================================
// ARCHIVO DE PRUEBA PARA ANÁLISIS SEMÁNTICO
// Proyecto de Lenguajes de Programación
// ============================================================================

// ============================================================================
// PRUEBAS VÁLIDAS (Sin errores semánticos)
// ============================================================================

// Variables y constantes válidas
var numero: Int = 10
let pi: Double = 3.14159
var mensaje: String = "Hola Mundo"
var esValido: Bool = true

// Uso correcto de variables declaradas
var suma: Int = numero + 5
print(suma)

// Función con tipo de retorno correcto
func sumar(a: Int, b: Int) -> Int {
    return a + b
}

// Uso de función declarada
var resultado: Int = sumar(5,3)

// Bucle for válido
for i in 1...5 {
    print(i)
}

// While con break válido
var contador: Int = 0
while contador < 10 {
    contador = contador + 1
    if contador == 5 {
        break
    }
}

// ============================================================================
// REGLA 1: USO DE IDENTIFICADORES NO DECLARADOS
// ============================================================================

// ERROR: Variable 'x' no declarada
var y: Int = x + 10

// ERROR: Uso de variable antes de declararla
print(variableNoDeclarada)

// ERROR: Llamada a función no declarada
funcionInexistente()

// ============================================================================
// REGLA 2: ASIGNACIÓN A UNA CONSTANTE
// ============================================================================

// Declarar constante
let constante: Int = 100

// ERROR: Intentar modificar constante
constante = 200

// ERROR: Operador compuesto en constante
constante += 50

// Otro ejemplo
let nombre: String = "Juan"
// ERROR: Reasignar constante
nombre = "Pedro"

// ============================================================================
// REGLA 3: INCOMPATIBILIDAD DE TIPOS EN OPERACIONES ARITMÉTICAS
// ============================================================================

var entero: Int = 10
var texto: String = "Hola"
var booleano: Bool = true




// ERROR: Multiplicar Bool con Int
var error2: Int = booleano * entero

// ERROR: Restar String con Int
var error3: Int = texto - entero

// ERROR: Dividir Bool con Double
var decimal: Double = 5.5
var error4: Double = booleano / decimal

// Operación válida
var suma2: Int = entero + 20

// ============================================================================
// REGLA 4: SENTENCIA BREAK O CONTINUE FUERA DE UN BUCLE
// ============================================================================

// ERROR: break fuera de bucle
var variable: Int = 5
break

// ERROR: continue fuera de bucle
continue

// ERROR: break en contexto incorrecto
func otraFuncion() -> Int {
    var x: Int = 10
    break
    return x
}

// ERROR: continue fuera de bucle dentro de función
func funcionConError() {
    
    continue
    print("Hola mundo")
}

// Uso correcto: break dentro de bucle
for j in 1...10 {
    if j == 5 {
        break
    }
}

// ============================================================================
// REGLA 5: TIPO DE RETORNO DE FUNCIÓN INCORRECTO
// ============================================================================

// ERROR: Función debe retornar Int pero retorna String
func obtenerNumero() -> Int {
    return "texto"
}

// ERROR: Función debe retornar String pero retorna Int
func obtenerTexto() -> String {
    return 42
}

// ERROR: Función con tipo de retorno pero no retorna nada
func calcular() -> Double {
    var x: Double = 5.5
    var y: Double = 2.2
    // Falta return
}

// ERROR: Función sin tipo de retorno pero retorna algo
func imprimirMensaje() {
    print("Mensaje")
    return 100
}

// ERROR: Tipo incorrecto en return
func esPar(num: Int) -> Bool {
    return num
}

// Función correcta
func multiplicar(a: Int, b: Int) -> Int {
    return a * b
}

// ============================================================================
// REGLA 6: REDECLARACIÓN DE VARIABLE EN EL MISMO ÁMBITO
// ============================================================================

// Primera declaración
var miVariable: Int = 10

// ERROR: Redeclarar en el mismo ámbito
var miVariable: Int = 20

// Primera constante
let miConstante: String = "valor1"

// ERROR: Redeclarar constante
let miConstante: String = "valor2"

// ERROR: Redeclarar con diferente tipo
var otraVariable: Int = 5
var otraVariable: String = "texto"

// Función con parámetro
func miFuncion(parametro: Int) -> Int {
    // ERROR: Redeclarar parámetro
    var parametro: Int = 100
    return parametro
}

// ERROR: Redeclarar función
func miFuncion(parametro: Int) -> Int {
    return parametro * 2
}

// ============================================================================
// CASOS ESPECIALES Y ÁMBITOS ANIDADOS
// ============================================================================

// Ámbito global
var global: Int = 100

func funcionConAmbitos() {
    // Ámbito de función - OK: puede declarar 'local'
    var local: Int = 50
    
    // Bucle anidado
    for i in 1...3 {
        // Ámbito de bucle - OK: puede usar 'local' del ámbito superior
        var temp: Int = local + i
        print(temp)
    }
    
    // ERROR: 'temp' no existe en este ámbito
    print(temp)
}


// ============================================================================
// FIN DEL ARCHIVO DE PRUEBA
// ============================================================================