# 🐉 DragonScript - Extensión de VS Code

Extensión de Visual Studio Code que proporciona soporte de sintaxis completo para el lenguaje de programación **DragonScript**, inspirado en el universo de Dragon Ball.

## ✨ Características

- 🎨 **Resaltado de sintaxis** completo para DragonScript
- 📝 **Snippets inteligentes** para construir código más rápido
- 🔧 **Auto-completado** de llaves, paréntesis y comillas
- 💬 **Soporte de comentarios** con `#`
- 📦 **Asociación de archivos** `.ds`
- 🎯 **Indentación automática** inteligente

## 🚀 Instalación

### Opción 1: Instalación desde VSIX (local)

1. Abre VS Code
2. Ve a la pestaña de Extensiones (`Ctrl+Shift+X`)
3. Haz clic en el menú `...` (arriba a la derecha)
4. Selecciona **"Instalar desde VSIX..."**
5. Navega a la carpeta `dragonscript-vscode-extension`
6. Selecciona el archivo `.vsix` (cuando lo generes)

### Opción 2: Instalación desde código fuente

1. Copia la carpeta `dragonscript-vscode-extension` a:
   - **Windows**: `%USERPROFILE%\.vscode\extensions\`
   - **macOS/Linux**: `~/.vscode/extensions/`

2. Reinicia VS Code

3. Abre cualquier archivo `.ds` y verás el resaltado de sintaxis activado

## 🎨 Temas de Color

La extensión funciona con cualquier tema de VS Code. Los colores recomendados son:

- **Keywords de control** (SENSAR, ENTRENAR, RASTREAR): Naranja brillante
- **Keywords de Dragon Ball** (KI, SCOUTER): Rojo
- **Strings**: Verde
- **Números**: Azul
- **Comentarios**: Gris

## 📝 Snippets Disponibles

Escribe estos prefijos y presiona `Tab` para autocompletar:

| Prefijo | Descripción |
|---------|-------------|
| `ki` | Declarar variable |
| `scouter` | Imprimir valor |
| `input` | Leer entrada del usuario |
| `sensar` | Condicional SENSAR |
| `sensaresquivar` | Condicional SENSAR-ESQUIVAR |
| `entrenar` | Bucle ENTRENAR (while) |
| `gravedad` | Bucle GRAVEDAD (repite N veces) |
| `rastrear` | Recorrido RASTREAR ... EN ... |
| `rango` | Rango de enteros `[inicio..fin]` |
| `tecnica` | Declarar función |
| `guerrero` | Declarar registro/clase |
| `evoluciona` | Guerrero con herencia |
| `invocar` | Crear objeto/registro |
| `legendario` | Método estático |
| `lista` | Declarar lista |

## 🔧 Configuración Adicional

Para una mejor experiencia, agrega esto a tu `settings.json` de VS Code:

```json
{
    "[dragonscript]": {
        "editor.tabSize": 4,
        "editor.insertSpaces": true,
        "editor.autoIndent": "full"
    }
}
```

## 🐛 Reportar Problemas

Si encuentras algún problema o tienes sugerencias, abre un issue en:
https://github.com/zeraus17/DragonScript/issues

## 📄 Licencia

MIT © 2026 zeraus17

---

**¡Disfruta programando con el poder de Dragon Ball! 🐉⚡**
