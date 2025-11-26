# Swift Analyzer

**Analizador Léxico, Sintáctico y Semántico para Swift**

Swift Analyzer es una herramienta que permite analizar código Swift a través de un lexer, un parser y un analizador semántico implementados en Python utilizando PLY. Incluye además una interfaz web sencilla para visualizar los resultados del análisis.

## Requisitos

* Python ≥ 3.11
* `ply`
* `uvicorn`
* `fastapi`


## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/alexoterol/a-lex-prog-lang.git
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```


## Uso

### Ejecución automática con Bash

Si tu sistema dispone de `bash`, simplemente ejecuta el script incluido:

```bash
bash run.sh
```

Esto levantará tanto el backend como el frontend de manera automática.

### Ejecución manual

Si no cuentas con `bash`, deberás iniciar ambos componentes por separado.

#### **1. Ejecutar el backend**

Desde el directorio principal:

```bash
cd src && uvicorn server.app:app --port 8000
```

#### **2. Ejecutar el frontend**

Desde el directorio principal:

```bash
python -m http.server 5500 --directory ./src/frontend
```

#### **3. Abrir la interfaz web**

Navega a:

```
http://localhost:5500/
```
