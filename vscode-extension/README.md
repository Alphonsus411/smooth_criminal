# Smooth Criminal VSCode Extension

Esta extensión analiza el código Python abierto en el editor activo y utiliza `smooth_criminal` para ofrecer sugerencias de optimización.

## Instalación

1. En la carpeta `vscode-extension` ejecuta:
   ```bash
   npm install
   npm run package
   ```
   Esto generará un archivo `.vsix` que puedes instalar en VSCode.

2. En VSCode ve a `Extensiones` > `...` > `Instalar desde VSIX` y selecciona el archivo generado.

## Uso

1. Abre un archivo Python.
2. Ejecuta el comando **Smooth Criminal: Analizar AST** (desde la paleta de comandos `Ctrl+Shift+P`).
3. Las sugerencias aparecerán como notificaciones decoradas con `@smooth` y `@jam`.

## Pruebas

Para ejecutar las pruebas de la extensión:

```bash
npm test
```
