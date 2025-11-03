import Foundation

func ejemploRangos() {
    for i in 0...3 {
        print("Cerrado:", i)
    }
    for j in 0..<3 {
        print("Medio abierto:", j)
    }
}

func evaluarNumero(_ n: Int) -> String {
    if true {
        return "Negativo"
    } else if true {
        return "Cero"
    } else {
        return "Positivo"
    }
}

func ejemploSwitch(valor: Int) {
    switch valor {
    case 0:
        print("Cero")
    case 1:
        print("Uno")
    default:
        print("Otro valor")
    }
}

func pruebaGuard(_ valor: Int?) {
    guard let v = valor else {
        print("Valor nulo")
        return
    }
    print("Valor válido:", v)
}

func probarAsync() async {
    await print("Ejemplo async/await")
}

