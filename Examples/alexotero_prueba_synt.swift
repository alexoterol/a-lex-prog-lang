// MARK: - 1. Inicialización de Variables y Diccionarios

// Diccionario [String: Int] (tipo explícito)
let userScores: [String: Int] = ["Alice": 95, "Bob": 88]

// Diccionario [String: Any] (inferencia de tipo con múltiples tipos de valor)
var profileData = ["name": "Carl", "isActive": true, "rank": 3]

// Variable opcional
var optionalKey: String? = nil

var currentScore = 95
var attempts = 4

// MARK: - 2. Estructura de Control: Funciones

// Funciones con parámetro opcional y valor por defecto
func calculateDiscount(price: Double, percentage: Double? = 0.1) -> Double {
    
    // Operador Nil-Coalescing (??)
    let finalPercentage = percentage ?? 0.05
    
    // Expresión booleana con múltiples conectores
    let isHighDiscount = (finalPercentage >= 0.1) && (price > 100)

    // Condicionales if-else if-else
    if isHighDiscount {
        return price * (1 - finalPercentage)
    } else if finalPercentage > 0 {
        return price * (1 - finalPercentage)
    } else {
        return price // Sin descuento
    }
}

// MARK: - 3. Estructura de Control: guard, while, if-else

func processGame(score: Int) {
    
    // Guard Statement
    guard score > 0 else {
        print("El juego debe tener un score positivo.")
        return // Transferencia de control obligatoria
    }
    
    // Bucle while con condiciones de bucle complejas
    while attempts > 0 && currentScore < 100 {
        
        // Acceso a valor por clave en diccionario
        let aliceScore = userScores["Alice"] ?? 0
        
        // Operador Ternario (? :)
        let newScore = (aliceScore > 90) ? aliceScore + 5 : aliceScore + 1
        
        // Reasignación para afectar el bucle
        currentScore = newScore
        attempts = attempts - 1
        
        // if-else
        if attempts == 0 {
            print("Último intento.")
        } else {
            print("Intentos restantes: \(attempts)")
        }
    }
}

// MARK: - 4. Llamadas y Pruebas de Expresiones
let finalPrice = calculateDiscount(price: 250, percentage: 0.2) // Llama con opcional (0.2)
let regularPrice = calculateDiscount(price: 50)               // Llama sin opcional (usa 0.1)

processGame(score: 100)