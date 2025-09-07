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
| `@jam(workers=n)`       | Paralelismo automático con ThreadPoolExecutor         |
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

- Botones para exportar CSV, limpiar historial o ver gráfico

- Interfaz elegante con Flet (modo oscuro)

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

Luego edita `.env` para personalizar valores como `LOG_PATH`.


## 💃 Ejemplo rápido

````python
from smooth_criminal import smooth, thriller

@thriller
@smooth
def square(n):
    return [i * i for i in range(n)]

print(square(10))
````

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

## 📚 Documentación

Próximamente en ReadTheDocs…

## 📝 Licencia

MIT © Adolfo González


## 🎤 Créditos

- Michael Jackson por la inspiración musical 🕺

- Numba, NumPy, asyncio por la base técnica

- Flet por el dashboard elegante

