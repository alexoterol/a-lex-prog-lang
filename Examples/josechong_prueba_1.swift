struct Punto {
    var x: Double
    var y: Double
}

class Rectangulo {
    var origen: Punto
    var ancho: Double
    var alto: Double

    init(origen: Punto, ancho: Double, alto: Double) {
        self.origen = origen
        self.ancho = ancho
        self.alto = alto
    }

    func area() -> Double {
        return ancho
    }
}

do {
    let r = Rectangulo(origen: Punto(x: 0, y: 0), ancho: 5.0, alto: 2.0)
    print("Área:", r.area())
    ejemploRangos()
    print(evaluarNumero(5))
    ejemploSwitch(valor: 2)
    pruebaGuard(nil)
} catch {
    print("Error capturado")
}
