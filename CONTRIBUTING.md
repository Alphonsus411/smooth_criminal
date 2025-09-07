# Guía de Contribución

¡Gracias por tu interés en mejorar Smooth Criminal!

## Configuración rápida

```bash
git clone https://github.com/Alphonsus411/smooth_criminal.git
cd smooth_criminal
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r docs/requirements.txt
pip install -e .
```

## Ejecutar pruebas

Antes de enviar cambios, verifica que todo funciona:

```bash
pytest
```

## Construir la documentación

```bash
sphinx-build -b html docs docs/_build/html
```

## Flujo de trabajo sugerido

1. Crea una rama descriptiva a partir de `main`.
2. Realiza tus cambios y actualiza `CHANGELOG.md`.
3. Añade tu nombre a `CONTRIBUTORS.md` si es tu primera aportación.
4. Ejecuta las pruebas y construye la documentación.
5. Abre un Pull Request explicando tu contribución.

¡Tu ayuda hace que el proyecto siga moviéndose al ritmo de MJ! 🕺
