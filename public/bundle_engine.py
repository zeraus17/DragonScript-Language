#!/usr/bin/env python3
"""Empaqueta el código fuente de DragonScript en un JS para el playground (Pyodide)."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAGONSCRIPT_DIR = ROOT / "dragonscript"
OUTPUT_JS = Path(__file__).parent / "dragonscript_engine.js"

files_data = {}

# Incluir todos los .py y .ds del paquete (incluyendo subdirectorios)
for file_path in DRAGONSCRIPT_DIR.rglob("*"):
    if file_path.suffix in (".py", ".ds") and "__pycache__" not in file_path.parts:
        # Clave relativa al paquete dragonscript/
        rel = file_path.relative_to(DRAGONSCRIPT_DIR).as_posix()
        files_data[rel] = file_path.read_text(encoding="utf-8")

js_content = (
    "window.DRAGONSCRIPT_FILES = "
    + json.dumps(files_data, ensure_ascii=False, indent=2)
    + ";\n"
)
OUTPUT_JS.write_text(js_content, encoding="utf-8")
print(f"✅ Motor empaquetado exitosamente ({len(files_data)} archivos) en: {OUTPUT_JS}")
