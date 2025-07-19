import json, pathlib, io

# -----------------------------------------------------------
# i18n helper (JSON)
# -----------------------------------------------------------
def load_lang(lang: str) -> dict:
    path = pathlib.Path(__file__).parent / "locales" / f"{lang}.json"
    return json.loads(path.read_text(encoding="utf-8"))



DEFAULT_HOLE_DIAMETER = 51        # mm
DEFAULT_EXPLOSIVE_DENSITY = 1.15  # g/cm³
DEFAULT_HOLE_DEPTH = 4.0          # m