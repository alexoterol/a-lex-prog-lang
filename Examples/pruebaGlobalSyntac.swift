// ============================================================================
// ARCHIVO DE PRUEBA GLOBAL - ANALIZADOR SINTÁCTICO
// Proyecto de Lenguajes de Programación - Swift
// ============================================================================
// INTEGRANTES:
// - Alexandre Icaza (aledicaz): Arrays, for-in, expresiones aritméticas, funciones
// - Alex Otero (alexoterol): Diccionarios, if-else, guard, while, operadores lógicos
// - Jose Chong (Jlchong3): POO, tuplas, switch-case, print/readLine
// ============================================================================

// ============================================================================
// 1. VARIABLES Y CONSTANTES (Alexandre + Alex O)
// ============================================================================
let maxUsers = 100
var currentUsers = 0
let pi: Double = 3.14159
var message: String = "Bienvenido"
var optionalValue: Int? = nil
let inferredValue = 42

// ============================================================================
// 2. EXPRESIONES ARITMÉTICAS (Alexandre)
// ============================================================================
let sum = 10 + 20
let difference = 50 - 15
let product = 5 * 8
let quotient = 100 / 4
let remainder = 17 % 5
let complex = (3 + 4) * 2 - 1
let negative = -10
let positive = +15

// ============================================================================
// 3. EXPRESIONES LÓGICAS Y BOOLEANAS (Alex O)
// ============================================================================
let isActive = true
let hasPermission = false
let canAccess = isActive && hasPermission
let shouldNotify = isActive || hasPermission
let isInactive = !isActive
let complexCondition = (currentUsers < maxUsers) && isActive

// ============================================================================
// 4. OPERADORES DE COMPARACIÓN (Alexandre + Alex O)
// ============================================================================
let isEqual = 10 == 10
let notEqual = 5 != 3
let greaterThan = 15 > 10
let lessThan = 5 < 20
let greaterOrEqual = 10 >= 10
let lessOrEqual = 8 <= 12

// ============================================================================
// 5. OPERADOR TERNARIO Y NIL-COALESCING (Alex O)
// ============================================================================
let age = 18
let status = age >= 18 ? "adult" : "minor"
let username = optionalValue ?? 0
let greeting = message ?? "Hello"

// ============================================================================
// 6. ARRAYS - ESTRUCTURA DE DATOS (Alexandre)
// ============================================================================
let numbers: [Int] = [1, 2, 3, 4, 5]
var names: [String] = ["Ana", "Bob", "Carol"]
let emptyArray: [Double] = []
var mixedArray = [10, 20, 30, 40]

let firstNumber = numbers[0]
let secondName = names[1]

// ============================================================================
// 7. DICCIONARIOS - ESTRUCTURA DE DATOS (Alex O)
// ============================================================================
let scores: [String: Int] = ["Alice": 95, "Bob": 87, "Carol": 92]
var userInfo: [String: String] = ["name": "John", "city": "NYC"]
let emptyDict: [String: Int] = [:]
var productPrices = ["laptop": 1200, "phone": 800]

let aliceScore = scores["Alice"]
let cityName = userInfo["city"]

// ============================================================================
// 8. TUPLAS - ESTRUCTURA DE DATOS (Jose)
// ============================================================================
let coordinates: (Double, Double) = (3.14, 2.71)
let person: (name: String, age: Int) = (name: "Ana", age: 25)
let mixedTuple = (42, "text", true)

let xCoord = coordinates.0
let yCoord = coordinates.1
let personName = person.name

// ============================================================================
// 9. BUCLE FOR-IN (Alexandre)
// ============================================================================
for i in 1...5 {
    let value = i * 2
}

for num in numbers {
    let square = num * num
}

for index in 0..<10 {
    let result = index + 1
}

// ============================================================================
// 10. CONDICIONALES IF-ELSE (Alex O)
// ============================================================================
if age >= 18 {
    let message = "You can vote"
}

if age >= 21 {
    let drink = "beer"
} else {
    let drink = "juice"
}

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

// ============================================================================
// 11. GUARD STATEMENTS (Alex O)
// ============================================================================
func checkAge(userAge: Int) {
    guard userAge >= 18 else {
        return
    }
    let canProceed = true
}

func validateName(name: String?) {
    guard name != nil else {
        return
    }
    let validName = name
}

// ============================================================================
// 12. BUCLE WHILE (Alex O)
// ============================================================================
var counter = 0
while counter < 5 {
    counter = counter + 1
}

var running = true
while running && counter > 0 {
    counter = counter - 1
    running = counter > 0
}

// ============================================================================
// 13. SWITCH-CASE (Jose)
// ============================================================================
let dayOfWeek = 3
switch dayOfWeek {
case 1, 7:
    let type = "Weekend"
case 2, 3, 4, 5, 6:
    let type = "Weekday"
default:
    let type = "Invalid"
}

let grade = "A"
switch grade {
case "A":
    let points = 4
case "B":
    let points = 3
case "C":
    let points = 2
default:
    let points = 0
}

// ============================================================================
// 14. FUNCIONES SIMPLES (Alexandre)
// ============================================================================
func add(a: Int, b: Int) -> Int {
    return a + b
}

func greet(name: String) -> String {
    return name
}

func calculate() {
    let result = 10 + 20
}

// ============================================================================
// 15. FUNCIONES CON PARÁMETROS OPCIONALES Y VALORES POR DEFECTO (Alex O)
// ============================================================================
func createUser(name: String, age: Int?) -> String {
    let userAge = age ?? 0
    return name
}

func buildMessage(text: String = "Hello", times: Int = 1) -> String {
    return text
}

func processData(value: Int, multiplier: Int = 2, offset: Int = 0) -> Int {
    return value * multiplier + offset
}

// ============================================================================
// 16. FUNCIONES COMBINADAS (Todos)
// ============================================================================
func findScore(name: String, allScores: [String: Int]) -> Int {
    let userScore = allScores[name] ?? 0
    
    if userScore >= 90 {
        return 5
    } else if userScore >= 80 {
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
    let result = value > threshold ? "High" : "Low"
    
    return result
}

// ============================================================================
// 17. ENTRADA/SALIDA: PRINT (Jose)
// ============================================================================
print("Hola Mundo")
print("El resultado es:", 42)
print(message)
print()

// ============================================================================
// 18. ENTRADA/SALIDA: READLINE (Jose)
// ============================================================================
let userInput = readLine()
let response = readLine()

// ============================================================================
// 19. PROGRAMACIÓN ORIENTADA A OBJETOS: CLASES (Jose)
// ============================================================================
class Person {
    var name: String
    var age: Int
    let id: String
    
    init(name: String, age: Int, id: String) {
        self.name = name
        self.age = age
        self.id = id
    }
    
    func greet() {
        let message = self.name
    }
    
    func celebrateBirthday() {
        self.age = self.age + 1
    }
}

class Student {
    var name: String
    var grades: [Int]
    
    var averageGrade: Int {
        get {
            let sum = 0
            return sum
        }
    }
    
    init(name: String) {
        self.name = name
        self.grades = []
    }
    
    func addGrade(grade: Int) {
        let newGrade = grade
    }
}

// ============================================================================
// 20. CLASE COMPLEJA CON TODOS LOS CONCEPTOS (Todos)
// ============================================================================
class DataProcessor {
    var data: [String: Int]
    var isActive: Bool
    let maxItems: Int
    
    init(maxItems: Int = 100) {
        self.data = [:]
        self.isActive = true
        self.maxItems = maxItems
    }
    
    func processItem(key: String, value: Int?) -> String {
        guard self.isActive else {
            return "Inactive"
        }
        
        let finalValue = value ?? 0
        self.data[key] = finalValue
        
        if finalValue > 50 {
            return "High"
        } else if finalValue > 25 {
            return "Medium"
        } else {
            return "Low"
        }
    }
    
    func analyze() {
        var total = 0
        
        for i in 0..<5 {
            total = total + i
        }
        
        while total > 0 {
            total = total - 1
        }
    }
}

// ============================================================================
// 21. ASIGNACIONES COMPUESTAS (Alexandre)
// ============================================================================
var x = 10
x = x + 5
x += 3
x -= 2
x *= 4
x /= 2
x %= 3

// ============================================================================
// 22. EJEMPLOS COMPLEJOS COMBINADOS (Todos)
// ============================================================================

// Función que combina arrays, diccionarios y control de flujo
func analyzeData(numbers: [Int], threshold: Int = 50) -> [String: Int] {
    var results: [String: Int] = [:]
    var count = 0
    
    for num in numbers {
        if num > threshold {
            count = count + 1
        }
    }
    
    results["high"] = count
    results["total"] = 0
    
    return results
}

// Función con tuplas y switch
func categorizePoint(point: (x: Int, y: Int)) -> String {
    let x = point.x
    let y = point.y
    
    switch x {
    case 0:
        return "Origin"
    case 1, 2, 3:
        return "Low"
    default:
        return "High"
    }
}

// ============================================================================
// 23. CONDICIONES COMPLEJAS (Alex O)
// ============================================================================
let complexLogic = (age >= 18 && isActive) || (!hasPermission && score > 50)
let chainedTernary = age >= 21 ? "adult" : age >= 13 ? "teen" : "child"

// ============================================================================
// FIN DEL ARCHIVO DE PRUEBA
// ============================================================================