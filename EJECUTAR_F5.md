# 🚀 Cómo ejecutar programas DragonScript con F5

Este proyecto ya está configurado para que puedas ejecutar tus archivos `.ds` presionando **F5** en VS Code.

## ▶️ Forma 1: Presionar F5 (Recomendado)

1. **Abrí el proyecto en VS Code**
   ```
   code DragonScript
   ```

2. **Abrí cualquier archivo `.ds`** (por ejemplo: `examples/inventario_interactivo.ds`)

3. **Presioná F5** → El archivo se ejecuta automáticamente en la terminal integrada

---

## ⚡ Forma 2: Ctrl+Shift+B (Build Task)

Otra opción es presionar **Ctrl+Shift+B** (ejecuta la tarea de "build" configurada, que en este caso ejecuta el archivo actual).

---

## 🔧 Configuración incluida

El proyecto ya incluye estos archivos de configuración en `.vscode/`:

### `.vscode/launch.json`
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Ejecutar archivo .ds actual",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "args": ["${file}"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### `.vscode/tasks.json`
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Ejecutar DragonScript",
            "type": "shell",
            "command": "python",
            "args": ["main.py", "${file}"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "problemMatcher": []
        }
    ]
}
```

---

## 📝 Probar el inventario interactivo

1. Abrí `examples/inventario_interactivo.ds`
2. Presioná **F5**
3. Usá el menú para:
   - Agregar productos
   - Realizar ventas
   - Buscar
   - Listar inventario
   - Ver alertas de stock bajo
   - Reponer stock

---

## 🛠️ Alternativa: Script .bat (Windows)

Si preferís usar un script directo, creá un archivo `ejecutar.bat` en la raíz:

```bat
@echo off
python main.py %1
pause
```

Luego arrastrá cualquier archivo `.ds` sobre `ejecutar.bat` para ejecutarlo.

---

## 💡 Tip: Snippets

Escribí estos prefijos en un archivo `.ds` y presioná **Tab**:

- `ki` → Declarar variable
- `input` → Leer entrada del usuario
- `scouter` → Mostrar salida
- `warrior` → Crear clase
- `create` → Crear objeto
- `method` → Agregar método
- `if` → Condicional

---

¡Listo! Ahora podés desarrollar y probar tus programas DragonScript rápidamente. 🐉⚡
