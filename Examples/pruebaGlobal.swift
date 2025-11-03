// Se hicieron las partes en separado y luego se unió todo lo trabajado en un solo archivo 

// Archivo de prueba global para el analizador léxico/sintáctico/semántico
// Integrantes: Jose Chong, Alexandre Icaza, Alex Otero
// Fecha: 02/11/2025

/// Esta función imprime un saludo simple.
/// - Parameters:
///   - name: nombre de la persona
/// - Returns: un mensaje de saludo
/// Este comentario tipo /// debería ser ignorado por el analizador léxico.

import Foundation

/* Comentario multilínea normal
   Debe ser ignorado completamente por el lexer.
   También probamos anidación:
   /* bloque interno */
*/

/** Comentario multilínea de documentación
    También debería ser ignorado.
*/


// =============================
// SECCIÓN 1: VARIABLES, TIPOS, ASIGNACIÓN BÁSICA
// =============================

let constanteInmutable = 10          // LET
var contador = 0                     // VAR
var nombreUsuario: String = "Ana"    // anotación con COLON y STRING
var edad = 21                        // inferido Int
var opcionalNombre: String? = nil    // uso de nil
var isActive: Bool = true            // true
var isBlocked: Bool = false          // false

// Asignación compuesta y operadores aritméticos
contador = contador + 1      // =
contador += 1                // +=
contador -= 2                // -=
contador *= 3                // *=
contador /= 2                // /=
contador %= 4                // %=

var a = 5
var b = 9
var suma = a + b             // +
var resta = a - b            // -
var producto = a * b         // *
var division = b / a         // /
var modulo = b % a           // %


// Operadores de comparación
let esMayor = a > b          // >
let esMenor = a < b          // <
let esIgual = a == b         // ==
let esDistinto = a != b      // !=
let mayorOIgual = a >= b     // >=
let menorOIgual = a <= b     // <=

// Operadores lógicos
let negado = !isActive               // !
let conjuncion = isActive && false  // &&
let disyuncion = isActive || true   // ||

// Operador ternario
let maxValor = a > b ? a : b        // ? :

// Nil-coalescing
let username: String? = nil
let usernameFinal = username ?? "Anonimo"  // ??

// Rango cerrado y semiabierto
let rangoCerrado = 1...5    // ...
let rangoSemiAbierto = 0..<10  // ..<


// =============================
// SECCIÓN 2: ESTRUCTURAS DE CONTROL
// =============================

if a > b && isActive {
    print("a es mayor que b y activo")
} else {
    print("caso else ejecutado")
}

// guard con return temprano
func validarEdad(_ edad: Int?) -> Bool {
    guard let real = edad else {
        print("Edad inválida")
        return false
    }
    return real >= 18
}

// while loop con break / continue
var i = 0
while i < 10 {
    i += 1

    if i == 3 {
        continue  // continue debe ser reconocido como IDENTIFIER por algunos analizadores
    }

    if i == 8 {
        break     // break igual
    }
}

// for-in usando rango
for n in 1...5 {
    print("n:", n)
}

// switch con case y default
let dia = 3
switch dia {
case 1, 7:
    print("Fin de semana")
case 2:
    print("Lunes falso (?)")
default:
    print("Día normal")
}


// =============================
// SECCIÓN 3: FUNCIONES, RETURN, THROW, DO/TRY/CATCH, ASYNC/AWAIT
// =============================

// Función simple con parámetros y retorno
func sumar(_ x: Int, _ y: Int) -> Int {
    return x + y
}

// Función que "lanza" errores
func puedeFallar(flag: Bool) throws -> String {
    if flag == false {
        throw NSError(domain: "demo", code: 1, userInfo: nil) // throw
    }
    return "OK"
}

// Uso de do / try / catch
func probarError() {
    do {
        let resultado = try puedeFallar(flag: false) // try
        print(resultado)
    } catch {
        print("Se capturó un error en catch")
    }

    defer {
        print("Esto se ejecuta al final del scope (defer)")
    }
}

// Función async/await simulada
public func fetchData() async throws -> String {
    defer {
        print("Cerrando recurso en defer async")
    }

    // Esperar algo asíncrono
    let valor = "dataRemota"
    return valor
}

async func usarFetch() {
    do {
        let data = try await fetchData() // await + try
        print(data)
    } catch {
        print("Error async")
    }
}


// =============================
// SECCIÓN 4: TIPOS (struct, class, enum, protocol, extension)
// =============================

protocol Logger {                  // protocol
    func log(_ message: String)    // func dentro de protocol
}

// enum con cases
enum EstadoApp {
    case idle
    case running
    case error(String)
}

// struct con propiedades, willSet / didSet, get / set
struct ContadorStruct {
    // static property
    static var instanciaGlobal = 0   // static

    // propiedad almacenada con observadores
    var valor: Int = 0 {
        willSet {                   // willSet
            print("willSet valor", newValue)
        }
        didSet {                    // didSet
            print("didSet valor", oldValue)
        }
    }

    // propiedad computada con get y set
    var doble: Int {
        get {                       // get
            return valor * 2
        }
        set {                       // set
            valor = newValue / 2
        }
    }

    // init explícito
    init(inicial: Int) {            // init
        self.valor = inicial        // self
    }

    // método normal
    func mostrar() -> String {
        return "Valor actual: " + String(valor)
    }
}

// class con niveles de acceso y self
public class ServicioRed {          // public class
    private var endpoint: String    // private
    internal var timeout: Int = 30  // internal

    init(endpoint: String) {
        self.endpoint = endpoint
    }

    func hacerPeticion() -> Bool {
        print("Llamando a", self.endpoint)
        return true
    }
}

// extension de class para agregar comportamiento extra
extension ServicioRed {             // extension
    func logEstado(logger: Logger) {
        logger.log("Estado OK")
    }
}


// =============================
// SECCIÓN 5: USO DE some (tipo opaco), self, etc.
// =============================

// Para el analizador léxico, solo necesitamos que el token SOME aparezca.

func construirValor() -> some Int { // some
    return 42
}

// Ejemplo de acceso a self explícito dentro de clase
class ContadorDeClicks {
    var clicks = 0

    func click() {
        self.clicks += 1
    }
}


// =============================
// SECCIÓN 6: COLECCIONES, DICCIONARIOS, TUPLAS
// =============================

let numeros = [1, 2, 3, 4, 5]
let usuario = ["name": "Ana", "role": "admin"]
let punto = (x: 10, y: 20)
let mezcla: [Any] = ["texto", 10, true]

var mutableDict = ["visitas": 1]
mutableDict["visitas"] = (mutableDict["visitas"] ?? 0) + 1

// Acceso a índices con rango semiabierto
let primerosTres = Array(numeros[0..<3])

// ============= FIN DEL ARCHIVO =============
