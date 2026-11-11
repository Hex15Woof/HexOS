import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "data" / "settings.json"

DEFAULTS = {
    "accent": "#2878E8",
    "wallpaper": "gradient",
    "show_seconds": False,
    "start_menu_open": False
}

def load_config():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return {**DEFAULTS, **data}
        except (OSError, json.JSONDecodeError):
            pass
    save_config(DEFAULTS)
    return DEFAULTS.copy()

def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
