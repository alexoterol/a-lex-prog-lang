// ============================================================================
// ARCHIVO DE PRUEBA CON ERRORES SINTÁCTICOS
// Para demostrar el manejo de errores del analizador
// ============================================================================

// ERROR 1: Falta tipo después de dos puntos
let name: = "John"

// ERROR 2: Falta llave de cierre en if
if age > 18 {
    let message = "Adult"

// ERROR 3: Operador inválido
let result = 10 @@ 5

// ERROR 4: Falta paréntesis de cierre
func calculate(a: Int, b: Int -> Int {
    return a + b
}

// ERROR 5: Palabra reservada mal escrita (esto podría ser un error léxico)
variable counter = 0

// ERROR 6: Falta dos puntos en case
switch day {
case 1
    let type = "Monday"
default:
    let type = "Other"
}

// ERROR 7: Falta expresión en asignación
let value =

// ERROR 8: Array sin cerrar
let numbers = [1, 2, 3

// ERROR 9: Diccionario con sintaxis incorrecta
let data = ["key" "value"]

// ERROR 10: Función sin llaves
func test()

// ERROR 11: Falta ELSE en guard
guard age >= 18 {
    return
}

// ERROR 12: While sin condición
while {
    let x = 1
}

// ERROR 13: For-in sin IN
for i 1...5 {
    let value = i
}

// ERROR 14: Return fuera de función (este sería error semántico más adelante)
return 42

// ERROR 15: Clase sin llave de apertura
class Person
    var name: String
}