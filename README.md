# 🎩 Smooth Criminal

**A Python performance acceleration toolkit with the soul of Michael Jackson.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 ¿Qué es esto?

**Smooth Criminal** es una librería de Python para acelerar funciones y scripts automáticamente usando:
- 🧠 [Numba](https://numba.pydata.org/)
- ⚡ Asyncio y threading
- 📊 Dashboard visual con [Flet](https://flet.dev)
- 🧪 Benchmarks y profiling
- 🎶 Estilo, carisma y mensajes inspirados en MJ

---

## 💡 Características principales

| Decorador / Función     | Descripción                                           |
|-------------------------|--------------------------------------------------------|
| `@smooth`               | Aceleración con Numba (modo sigiloso y rápido)        |
| `@vectorized`          | Vectoriza funciones estilo NumPy con *fallback*       |
| `@guvectorized`        | Generaliza ufuncs con *fallback* seguro               |
| `@moonwalk`             | Convierte funciones en corutinas `async` sin esfuerzo |
| `@thriller`             | Benchmark antes y después (con ritmo)                 |
| `@jam(workers=n, backend="thread|process|async")` | Paralelismo con hilos, procesos o asyncio (cola dinámica) |
| `@black_or_white(mode)` | Optimiza tipos numéricos (`float32` vs `float64`)     |
| `@bad`                  | Modo de optimización agresiva (`fastmath`)            |
| `@beat_it`              | Fallback automático si algo falla                     |
| `dangerous(func)`       | Mezcla poderosa de decoradores (`@bad + @thriller`)   |
| `@bad_and_dangerous`    | Optimiza, perfila y maneja errores automáticamente    |
| `profile_it(func)`      | Estadísticas detalladas de rendimiento                |
| `analyze_ast(func)`     | Análisis estático para detectar código optimizable    |

---

## 🧠 Dashboard visual

Ejecuta el panel interactivo para ver métricas de tus funciones decoradas:

```bash
python -m smooth_criminal.dashboard
```
O bien:

````bash
python scripts/example_flet_dashboard.py
````

- Tabla con tiempos, decoradores y puntuaciones

- Botones para exportar CSV/JSON/XLSX/MD, limpiar historial o ver gráfico

- Interfaz elegante con Flet (modo oscuro)

### 🕺 Animación Moonwalk

Activa el interruptor **Moonwalk** para ver cómo un ícono de MJ cruza la
pantalla y desaparece al finalizar.

Prueba manual:

1. Ejecuta `python -m smooth_criminal.dashboard` o `python scripts/example_flet_dashboard.py`.
2. Pulsa el interruptor **Moonwalk** en la fila de botones.
3. Observa al bailarín deslizarse y liberarse automáticamente.

## ⚙️ Instalación

````bash
pip install smooth-criminal
````

O para desarrollo local:

````bash
git clone https://github.com/Alphonsus411/smooth_criminal.git
cd smooth_criminal
pip install -e .
````


## 🛠️ Configuración de entorno

Antes de ejecutar la librería copia el archivo de ejemplo y ajusta las variables:

````bash
cp .env.example .env
````

Dentro de `.env` puedes definir:

```
# Ruta donde se guardan las métricas
LOG_PATH=.smooth_criminal_log.json

# Backend de almacenamiento: json (por defecto), sqlite o tinydb
SMOOTH_CRIMINAL_STORAGE=json
```

Para backend `tinydb` instala la dependencia opcional `tinydb` y para exportar a
`xlsx` instala `openpyxl`.


## 💃 Ejemplo rápido

````python
from smooth_criminal import smooth, thriller

@thriller
@smooth
def square(n):
    return [i * i for i in range(n)]

print(square(10))
````

### 🎷 Paralelismo con `jam`

```python
from smooth_criminal.core import jam

@jam(workers=4, backend="process")
def cube(x):
    return x ** 3

print(cube([1, 2, 3]))

# También disponible backend="thread" (por defecto) o backend="async"
```

### ⏱️ Benchmark de backends con `benchmark_jam`

```python
from smooth_criminal.benchmark import benchmark_jam, detect_fastest_backend

def cube(x):
    return x ** 3

data = benchmark_jam(cube, [1, 2, 3], ["thread", "process", "async"])
print(data["fastest"])            # backend más veloz

best = detect_fastest_backend(cube, [1, 2, 3], ["thread", "process", "async"])
print(best)
```

## 🚧 Modo bad_and_dangerous

````python
from smooth_criminal import bad_and_dangerous

def fallback(_):
    return -1

@bad_and_dangerous(fallback=fallback)
def risky(n):
    total = 0
    for i in range(n):
        total += i
    return total

print(risky(5))
````

## 🧮 Vectorización segura

````python
import numpy as np
from smooth_criminal import vectorized, guvectorized


@vectorized(["float64(float64)"])
def doble(x):
    return x * 2


@guvectorized(["void(float64[:], float64[:], float64[:])"], "(n),(n)->(n)")
def suma(a, b, res):
    for i in range(a.shape[0]):
        res[i] = a[i] + b[i]


print(doble(np.array([1.0, 2.0])))
print(suma(np.array([1.0, 2.0]), np.array([3.0, 4.0])))
````

## 🧪 CLI interactiva

````bash
smooth-criminal analyze my_script.py
````

Esto analizará tu código buscando funciones lentas, bucles, range(), etc.

Para exportar el historial en distintos formatos:

````bash
smooth-criminal export history.xlsx --format xlsx
smooth-criminal export history.md --format md
smooth-criminal export history.json --format json
````

También puedes comparar rápidamente los backends de `jam` desde la línea de comandos:

````bash
smooth-criminal jam-test paquete.modulo:funcion --workers 4 --reps 3
````

Si prefieres un resultado en JSON sin mensajes adicionales, añade `--silent`:

````bash
smooth-criminal jam-test paquete.modulo:funcion --workers 4 --reps 3 --silent
````

Esto mostrará una tabla comparativa de tiempos y, al finalizar sin errores, el mensaje especial:

```
🎶 Just jammin' through those CPU cores! 🧠🕺
```

### 🕺 Modo MJ

Activa efectos especiales al detectar mejoras de rendimiento:

```bash
smooth-criminal jam-test paquete.modulo:funcion --workers 4 --mj-mode
```

Cuando el modo está activo y el rendimiento mejora al menos un 10 %, se
reproducirá un pequeño efecto de Michael Jackson.  Si la dependencia
`playsound` no está disponible, se mostrará un mensaje o GIF/ASCII mediante
`rich`.  En ausencia de estas dependencias, solo se emitirá una advertencia.

## 💾 Backends de almacenamiento

El historial de ejecuciones se guarda usando un backend configurable.
Selecciona el backend con la variable de entorno `SMOOTH_CRIMINAL_STORAGE`:

````bash
export SMOOTH_CRIMINAL_STORAGE=sqlite  # json | sqlite | tinydb
smooth-criminal analyze my_script.py
````

El backend `sqlite` no requiere extras. Para `tinydb` instala `tinydb` y para
exportar a `xlsx` instala `openpyxl`.

## 📚 Documentación

Próximamente en ReadTheDocs…

## 📝 Licencia

MIT © Adolfo González


## 🎤 Créditos

- Michael Jackson por la inspiración musical 🕺

- Numba, NumPy, asyncio por la base técnica

- Flet por el dashboard elegante

