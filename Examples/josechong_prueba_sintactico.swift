// Archivo de prueba para analizador sintáctico
// Integrante: [Tu Nombre]
// Prueba: Entrada/Salida, POO, Tuplas, Switch-Case

// ==========================================
// PRUEBA 1: ENTRADA/SALIDA - PRINT
// ==========================================

print()
print(5)
print(10, 20, 30)
print(mensaje)


// ==========================================
// PRUEBA 2: ENTRADA/SALIDA - READLINE
// ==========================================

readLine()


// ==========================================
// PRUEBA 3: TUPLAS - DECLARACIÓN Y ACCESO
// ==========================================

// Tupla simple con valores
let coordenadas: (Int, Int)
coordenadas.0
coordenadas.1

// Tupla nombrada
let persona: (nombre: String, edad: Int)
persona.nombre
persona.edad

// Otra tupla
let punto: (x: Int, y: Int)
punto.x
punto.y


// ==========================================
// PRUEBA 4: SWITCH-CASE SIMPLE
// ==========================================

switch numero {
case 1:
    print(1)
case 2:
    print(2)
case 3:
    print(3)
default:
    print(0)
}


// ==========================================
// PRUEBA 5: SWITCH CON CASOS MÚLTIPLES
// ==========================================

switch letra {
case a, b, c:
    print(1)
case d, e:
    print(2)
default:
    print(0)
}


// ==========================================
// PRUEBA 6: CLASE BÁSICA CON PROPIEDADES
// ==========================================

class Persona {
    var nombre: String
    var edad: Int
    let id: Int
}


// ==========================================
// PRUEBA 7: CLASE CON INICIALIZADOR
// ==========================================

class Estudiante {
    var nombre: String
    var nota: Int

    init(nombre: String, nota: Int) {
        self.nombre
        self.nota
    }
}


// ==========================================
// PRUEBA 8: CLASE CON MÉTODOS Y SELF
// ==========================================

class Calculadora {
    var resultado: Int

    init() {
        self.resultado
    }

    func mostrarResultado() {
        print(self.resultado)
    }

    func resetear() {
        self.resultado
        print(0)
    }
}


// ==========================================
// PRUEBA 9: PROPIEDAD COMPUTADA
// ==========================================

class Rectangulo {
    var ancho: Int
    var alto: Int

    var area: Int {
        get {
            return self.ancho
        }
    }
}


// ==========================================
// PRUEBA 10: CLASE COMPLETA CON TODO
// ==========================================

class CuentaBancaria {
    var titular: String
    var saldo: Double
    let numeroCuenta: Int

    init(titular: String, numero: Int) {
        self.titular
        self.numeroCuenta
        self.saldo
    }

    func depositar(monto: Double) {
        self.saldo
        print(self.saldo)
    }

    func consultarSaldo() {
        print(self.saldo)
        return self.saldo
    }

    func mostrarInfo() {
        print(self.titular)
        print(self.numeroCuenta)
        print(self.saldo)
    }
}


// ==========================================
// PRUEBA 11: MÚLTIPLES CLASES
// ==========================================

class Producto {
    var nombre: String
    var precio: Double

    init(nombre: String, precio: Double) {
        self.nombre
        self.precio
    }
}

class Tienda {
    var nombre: String
    var productos: Int

    init(nombre: String) {
        self.nombre
        self.productos
    }

    func agregarProducto() {
        self.productos
        print(self.productos)
    }
}


// ==========================================
// PRUEBA 12: SWITCH DENTRO DE MÉTODO
// ==========================================

class Sistema {
    var estado: String

    init(estado: String) {
        self.estado
    }

    func verificarEstado() {
        switch self.estado {
        case activo:
            print(1)
        case pausado:
            print(2)
        case inactivo:
            print(0)
        default:
            print(99)
        }
    }
}


// ==========================================
// PRUEBA 13: COMBINACIÓN PRINT + READLINE
// ==========================================

class Menu {
    var opcion: Int

    init() {
        self.opcion
    }

    func mostrarMenu() {
        print(1)
        print(2)
        print(3)
    }

    func leerOpcion() {
        readLine()
        self.opcion
    }
}


// ==========================================
// PRUEBA 14: TUPLAS Y MÉTODOS
// ==========================================

class Coordenadas {
    var punto: (x: Int, y: Int)

    init(x: Int, y: Int) {
        self.punto
    }

    func obtenerX() {
        return self.punto.x
    }

    func obtenerY() {
        return self.punto.y
    }

    func mostrarPunto() {
        print(self.punto.x, self.punto.y)
    }
}
