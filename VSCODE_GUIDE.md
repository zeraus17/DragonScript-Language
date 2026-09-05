# 🐉 Guía Completa: Usar DragonScript en Visual Studio Code

Esta guía te enseña cómo configurar y usar DragonScript en VS Code de la manera más cómoda posible.

---

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

1. ✅ **Python 3.8 o superior** → [Descargar aquí](https://www.python.org/downloads/)
   - Durante la instalación, marca **"Add Python to PATH"**
   
2. ✅ **Visual Studio Code** → [Descargar aquí](https://code.visualstudio.com/)

3. ✅ **DragonScript** (este proyecto descargado y descomprimido)

---

## 🚀 Configuración Inicial (Solo una vez)

### Paso 1: Abrir el Proyecto en VS Code

1. Abre **Visual Studio Code**
2. Ve a **File → Open Folder...** (o `Ctrl+K Ctrl+O`)
3. Navega a la carpeta `DragonScript` que descargaste
4. Haz clic en **Seleccionar carpeta**

### Paso 2: Instalar la Extensión de DragonScript

Tienes **2 opciones**:

#### Opción A: Instalación Rápida (Recomendada)

1. En VS Code, presiona `Ctrl+Shift+P` para abrir la paleta de comandos
2. Escribe: `Extensions: Install from VSIX...`
3. Navega a `DragonScript/dragonscript-vscode-extension/`
4. Si no hay archivo `.vsix`, **usa la Opción B**

#### Opción B: Instalación Manual

1. Copia la carpeta `dragonscript-vscode-extension` completa
2. Pégala en tu carpeta de extensiones de VS Code:
   - **Windows**: `C:\Users\TuNombre\.vscode\extensions\`
   - **macOS**: `~/.vscode/extensions/`
   - **Linux**: `~/.vscode/extensions/`
3. Renombra la carpeta a: `dragonscript-0.1.0`
4. Reinicia VS Code

### Paso 3: Verificar que Funciona

1. Abre cualquier archivo `.ds` en la carpeta `examples/`
2. **Deberías ver colores** en las palabras clave (KI, SCOUTER, IF, etc.)
3. Si no ves colores, reinicia VS Code

---

## ⚡ Ejecutar Programas DragonScript

### Método 1: Atajo de Teclado (Más Rápido) ⭐

1. Abre un archivo `.ds` (por ejemplo: `examples/hello.ds`)
2. Presiona **`Ctrl+Shift+B`** (Windows/Linux) o **`Cmd+Shift+B`** (macOS)
3. La salida aparecerá en el **Terminal** de VS Code

**¡Listo!** Este es el método más rápido para probar tu código.

### Método 2: Menú de Tareas

1. Presiona **`Ctrl+Shift+P`** para abrir la paleta de comandos
2. Escribe: `Tasks: Run Task`
3. Selecciona: **"Ejecutar DragonScript"**

### Método 3: Terminal Manual

1. Abre el terminal integrado: **`Ctrl+Ñ`** o **View → Terminal**
2. Ejecuta:
   ```bash
   python main.py examples/hello.ds
   ```

### Método 4: Debug/Run (F5)

1. Abre un archivo `.ds`
2. Presiona **`F5`**
3. Selecciona: **"DragonScript: Ejecutar archivo actual"**
4. La salida aparecerá en el terminal

---

## 🎮 Usar el REPL Interactivo

El REPL te permite probar código DragonScript línea por línea.

### Iniciar el REPL:

**Opción 1: Desde Tareas**
1. `Ctrl+Shift+P` → `Tasks: Run Task`
2. Selecciona: **"Abrir REPL de DragonScript"**

**Opción 2: Desde Terminal**
```bash
python main.py --repl
```

### Ejemplo de uso:

```dragonscript
DragonScript REPL v0.1.0
Usa 'exit()' para salir

>>> KI power = 9000
>>> SCOUTER power
9000

>>> IF power > 8000 {
...     SCOUTER "¡Es más de 8000!"
... }
¡Es más de 8000!

>>> TECHNIQUE sumar(a, b) {
...     RETURN a + b
... }

>>> SCOUTER sumar(5, 10)
15
```

Para salir del REPL:
- Escribe `exit()` y presiona Enter
- O presiona `Ctrl+C` dos veces

---

## 📝 Snippets: Escribe Código Más Rápido

Los **snippets** son plantillas de código que se autocompletan.

### Cómo usarlos:

1. En un archivo `.ds`, escribe el **prefijo**
2. Presiona **`Tab`**
3. El código se autocompletará

### Lista de Snippets Disponibles:

| Escribe | Presiona Tab | Obtienes |
|---------|--------------|----------|
| `ki` | Tab | `KI nombre = valor` |
| `scouter` | Tab | `SCOUTER expresion` |
| `if` | Tab | Bloque IF completo |
| `ifelse` | Tab | Bloque IF-ELSE |
| `while` | Tab | Bucle WHILE |
| `gravity` | Tab | `GRAVITY N { }` |
| `technique` | Tab | Declaración de función completa |
| `warrior` | Tab | `WARRIOR nombre` |
| `transform` | Tab | `TRANSFORM guerrero -> transformacion` |
| `array` | Tab | `KI nombre = [elementos]` |

### Ejemplo Visual:

```
1. Escribe: ki
2. Presiona: Tab
3. Resultado: KI |nombre| = |valor|
   (con el cursor en 'nombre', listo para escribir)
```

---

## 🧪 Ejecutar Tests

### Opción 1: Desde Tareas
1. `Ctrl+Shift+P` → `Tasks: Run Task`
2. Selecciona: **"Ejecutar Tests de DragonScript"**

### Opción 2: Terminal
```bash
python -m unittest discover tests
```

### Salida esperada:
```
...............................................
----------------------------------------------------------------------
Ran 46 tests in 0.XYZ s

OK
```

---

## 🎨 Personalizar Colores

Si quieres cambiar los colores del resaltado de sintaxis:

1. Abre **Configuración**: `Ctrl+,`
2. Busca: `editor.tokenColorCustomizations`
3. Agrega/modifica:

```json
{
    "editor.tokenColorCustomizations": {
        "textMateRules": [
            {
                "scope": "keyword.control.dragonscript",
                "settings": {
                    "foreground": "#FF9800",
                    "fontStyle": "bold"
                }
            },
            {
                "scope": "keyword.other.dragonscript",
                "settings": {
                    "foreground": "#F44336",
                    "fontStyle": "bold"
                }
            }
        ]
    }
}
```

---

## 🔧 Atajos de Teclado Personalizados

Puedes crear tus propios atajos para ejecutar DragonScript más rápido.

1. Ve a **File → Preferences → Keyboard Shortcuts** (`Ctrl+K Ctrl+S`)
2. Busca: `Tasks: Run Build Task`
3. Haz clic en el ícono de lápiz y asigna tu atajo favorito

**Sugerencias:**
- `Ctrl+Alt+R` para ejecutar
- `Ctrl+Alt+I` para REPL

---

## 📂 Estructura de Archivos Recomendada

```
DragonScript/
├── .vscode/                    # Configuración de VS Code (ya incluida)
│   ├── tasks.json              # Tareas personalizadas
│   ├── launch.json             # Configuración de debug
│   └── settings.json           # Ajustes del proyecto
│
├── dragonscript/               # Motor del lenguaje (NO tocar)
├── examples/                   # Ejemplos para aprender
│   ├── hello.ds
│   ├── variables.ds
│   ├── control_flow.ds
│   └── functions.ds
│
├── tests/                      # Tests del lenguaje
│
├── mis_programas/              # TUS programas (crea esta carpeta)
│   ├── mi_primer_programa.ds
│   └── juego.ds
│
└── main.py                     # Intérprete principal
```

**💡 Consejo:** Crea una carpeta `mis_programas/` para tus propios programas y mantén separados los ejemplos.

---

## 🐛 Solución de Problemas

### ❌ "python no se reconoce como comando"

**Solución:**
1. Verifica que Python esté instalado: abre CMD y escribe `python --version`
2. Si falla, reinstala Python marcando **"Add Python to PATH"**
3. Reinicia VS Code

### ❌ No veo colores en los archivos .ds

**Solución:**
1. Verifica que la extensión esté instalada en `%USERPROFILE%\.vscode\extensions\`
2. El nombre de la carpeta debe ser `dragonscript-0.1.0`
3. Reinicia VS Code completamente
4. Abre un archivo `.ds` y en la esquina inferior derecha debería decir "DragonScript"

### ❌ "Ctrl+Shift+B no hace nada"

**Solución:**
1. Asegúrate de estar **dentro de la carpeta DragonScript** en VS Code
2. Verifica que el archivo `.vscode/tasks.json` existe
3. Abre un archivo `.ds` antes de presionar el atajo

### ❌ Los snippets no funcionan

**Solución:**
1. Escribe el prefijo completo (ejemplo: `technique`)
2. Presiona `Tab`, NO Enter
3. Si no funciona, presiona `Ctrl+Space` después de escribir el prefijo

---

## 📚 Recursos Adicionales

- **Documentación completa**: Lee el `README.md` principal
- **Ejemplos**: Revisa todos los archivos en `examples/`
- **Sintaxis del lenguaje**: Consulta la sección de referencia en el README

---

## 🎯 Resumen Rápido

**Para empezar a programar:**
1. Abre VS Code en la carpeta `DragonScript`
2. Instala la extensión (carpeta `dragonscript-vscode-extension`)
3. Abre `examples/hello.ds`
4. Presiona `Ctrl+Shift+B`
5. ¡Ya estás ejecutando DragonScript! 🐉

**Atajo más importante:**
- **`Ctrl+Shift+B`** = Ejecutar archivo actual

---

**¡Feliz programación con el poder de Dragon Ball! 🐉⚡**

¿Necesitas ayuda? Abre un issue en: https://github.com/zeraus17/DragonScript/issues
