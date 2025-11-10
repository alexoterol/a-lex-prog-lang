// Archivo de prueba para analizador sintáctico
// Integrante: Alexandre Icaza
// Prueba: Expresiones, Variables, Arrays, For-in, Funciones

// ========================================
// 1. DECLARACIÓN DE VARIABLES
// ========================================

// Variables con tipo explícito
let edad: Int = 25
var nombre: String = "Alexandre"
let precio: Double = 19.99
var activo: Bool = true

// Variables con inferencia de tipo
let cantidad = 100
var total = 0

// ========================================
// 2. EXPRESIONES ARITMÉTICAS
// ========================================

// Operaciones básicas
let suma = 10 + 5
let resta = 20 - 8
let multiplicacion = 6 * 7
let division = 100 / 4
let modulo = 17 % 5

// Expresiones complejas
let resultado = 2 + 3 * 4
let calculo = (10 + 5) * 2
let complejo = 100 - 20 * 3 + 8 / 2

// Expresiones con variables
let a = 5
let b = 10
let c = a + b * 2

// ========================================
// 3. ASIGNACIÓN DE VARIABLES
// ========================================

// Asignación simple
var contador = 0

// Asignación compuesta
contador += 5
contador -= 2
contador *= 3
contador /= 2
contador %= 4

// ========================================
// 4. ARRAYS - ESTRUCTURA DE DATOS
// ========================================

// Declaración de arrays
let numeros: [Int] = [1, 2, 3, 4, 5]
var nombres: [String] = ["Ana", "Luis", "María"]
let vacio: [Int] = []

// Array con inferencia de tipo
let valores = [10, 20, 30, 40]

// Acceso a elementos
let primero = numeros[0]
let segundo = valores[1]

// ========================================
// 5. BUCLE FOR-IN - ESTRUCTURA DE CONTROL
// ========================================

// For-in con rango cerrado
for i in 1...5 {
    total += i
}

// For-in con rango semiabierto
for j in 0..<10 {
    contador += 1
}

// For-in con array
for numero in numeros {
    let doble = numero * 2
}

// For-in anidado
for x in 1...3 {
    for y in 1...3 {
        let producto = x * y
    }
}

// ========================================
// 6. FUNCIONES
// ========================================

// Función simple con retorno
func suma(a: Int, b: Int) -> Int {
    return a + b
}

// Función sin parámetros
func saludar() -> String {
    return "Hola"
}

// Función sin retorno explícito
func imprimir(x: Int) {
    let resultado = x * 2
}

// Función con múltiples parámetros
func calcular(x: Int, y: Int, z: Int) -> Int {
    return x + y * z
}

// Función más compleja
func procesarArray(datos: [Int]) -> Int {
    var suma = 0
    for valor in datos {
        suma += valor
    }
    return suma
}

// ========================================
// 7. CASOS COMPLEJOS
// ========================================

// Expresiones con comparación
let mayor = 10 > 5
let igual = edad == 25
let diferente = cantidad != 0

// Expresiones unarias
let negativo = -10
let positivo = +5

// Combinación de todo
func factorial(n: Int) -> Int {
    var resultado = 1
    for i in 1...n {
        resultado *= i
    }
    return resultado
}

// Array de resultados
let resultados: [Int] = [suma, resta, multiplicacion]

// For con expresiones complejas
for indice in 0..<5 {
    let valor = indice * 2 + 1
    total += valor
}