import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DRAGONSCRIPT_DIR = ROOT / "dragonscript"
OUTPUT_JS = Path(__file__).parent / "dragonscript_engine.js"

files_data = {}

for file_path in DRAGONSCRIPT_DIR.glob("*"):
    if file_path.suffix in [".py", ".ds"] and file_path.name != "__pycache__":
        files_data[file_path.name] = file_path.read_text(encoding="utf-8")

js_content = f"window.DRAGONSCRIPT_FILES = {json.dumps(files_data, ensure_ascii=False, indent=2)};"
OUTPUT_JS.write_text(js_content, encoding="utf-8")

print(f"✅ Motor empaquetado exitosamente en: {OUTPUT_JS}")