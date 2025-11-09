// MARK: - 🚀 Pruebas de Asignación y Declaración de Variables en Swift

// 1. Constantes (let) con asignación directa
let maxItems = 100
let appVersion = 3.1
let isDebugMode = true

// 2. Variables (var) con tipo explícito e inicialización
var currentUserName: String = "Ricardo"
var totalScore: Int = 500
var temperatureCelsius: Double = 25.5

// 3. Variables con tipo inferido (Swift deduce el tipo por el valor inicial)
var message = "Bienvenido al sistema." // Infiere String
var currentYear = 2025 // Infiere Int
var rate = 0.75 // Infiere Double

// 4. Múltiples declaraciones en una sola línea (tanto constantes como variables)
let hour = 14, minute = 30, second = 0
var red = 255, green = 128, blue = 64

// 5. Asignación de Opcionales (Tipos que pueden contener 'nil')
var userAge: Int? = 30 // Inicializado con un valor (no es nil)
var website: String? = nil // Inicializado explícitamente como nil (vacío)

// 6. Asignación mediante una expresión (el resultado de la expresión se asigna)
let area = 5 * 8 // El resultado de la multiplicación (40) se asigna a area
var discountPrice = 100 - (100 * 0.15) // El resultado de la resta se asigna a discountPrice

// 7. Tuplas (Declaración de múltiples valores relacionados como una sola unidad)
let http404Error = (404, "Not Found") // Infiere (Int, String)
var userLocation = (latitude: 34.0, longitude: -118.0) // Tupla con nombres de elementos

// 8. Reasignación (solo permitido para variables 'var')
totalScore = totalScore + 100 // totalScore ahora es 600
