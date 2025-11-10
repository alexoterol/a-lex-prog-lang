// ============================================================================
// ARCHIVO DE PRUEBA - INTEGRANTE 2
// Control de Flujo y Lógica
// ============================================================================

// 1. EXPRESIONES BOOLEANAS Y OPERADORES LÓGICOS
let isValid = true && false || !false
let hasAccess = true && (false || true)
let result = !false && true

// 2. OPERADOR TERNARIO
let age = 18
let status = age >= 18 ? "adult" : "minor"
let max = 10 > 5 ? 10 : 5

// 3. NIL-COALESCING OPERATOR
let optionalName = nil
let name = optionalName ?? "Guest"
let value = 42 ?? 0

// 4. DICCIONARIOS - DECLARACIÓN E INICIALIZACIÓN
let scores: [String: Int] = ["Alice": 95, "Bob": 87, "Carol": 92]
var userInfo: [String: String] = ["name": "John", "city": "NYC"]
let emptyDict: [String: Int] = [:]
var mixedDict = ["count": 5, "total": 100]

// 5. DICCIONARIOS - ACCESO POR CLAVE
let aliceScore = scores["Alice"]
let userName = userInfo["name"]
let missing = scores["David"] ?? 0

// 6. CONDICIONALES IF-ELSE
if age >= 18 {
    let message = "You can vote"
}

if age >= 21 {
    let drink = "beer"
} else {
    let drink = "juice"
}

// 7. IF-ELSE IF-ELSE
let score = 85
if score >= 90 {
    let grade = "A"
} else if score >= 80 {
    let grade = "B"
} else if score >= 70 {
    let grade = "C"
} else {
    let grade = "F"
}

// 8. GUARD STATEMENTS
func checkAge(age: Int) {
    guard age >= 18 else {
        return
    }
    let canProceed = true
}

func validateUser(name: String?) {
    guard name != nil else {
        return
    }
    let validName = name
}

// 9. BUCLE WHILE
var counter = 0
while counter < 5 {
    counter = counter + 1
}

var running = true
while running && counter > 0 {
    counter = counter - 1
    running = counter > 0
}

// 10. FUNCIONES CON PARÁMETROS OPCIONALES
func greet(name: String?) -> String {
    let finalName = name ?? "Guest"
    return finalName
}

func createUser(name: String, age: Int?) -> String {
    let userAge = age ?? 0
    return name
}

// 11. FUNCIONES CON VALORES POR DEFECTO
func calculate(a: Int, b: Int = 10) -> Int {
    return a + b
}

func buildMessage(text: String = "Hello", times: Int = 1) -> String {
    return text
}

func processData(value: Int, multiplier: Int = 2, offset: Int = 0) -> Int {
    return value * multiplier + offset
}

// 12. COMBINANDO CARACTERÍSTICAS
func findScore(name: String, scores: [String: Int]) -> Int {
    let score = scores[name] ?? 0
    
    if score >= 90 {
        return 5
    } else if score >= 80 {
        return 4
    } else {
        return 3
    }
}

func validateAndProcess(data: Int?, threshold: Int = 50) -> String {
    guard data != nil else {
        return "Invalid"
    }
    
    let value = data ?? 0
    let status = value > threshold ? "High" : "Low"
    
    return status
}

// 13. LÓGICA COMPLEJA
let complexCondition = (age >= 18 && hasAccess) || (!isValid && score > 50)
let chainedTernary = age >= 21 ? "adult" : age >= 13 ? "teen" : "child"

// 14. WHILE CON CONDICIONES COMPLEJAS
var attempts = 0
var success = false
while attempts < 3 && !success {
    attempts = attempts + 1
    success = attempts >= 2
}