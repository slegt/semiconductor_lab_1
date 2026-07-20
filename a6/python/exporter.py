import json
import os
import re
from pathlib import Path
from typing import Any, Dict

import numpy as np

current_file = Path(__file__).resolve().parent
destination = current_file.parent / "plots" / "export.json"

# Beträge außerhalb dieses Bereichs werden in Exponentialschreibweise
# geschrieben, damit die JSON-Datei lesbar bleibt (z.B. 7.39e+10 statt
# 73872613828.30818). Alles dazwischen bleibt als Dezimalzahl.
SCI_UPPER = 1e5
SCI_LOWER = 1e-4
_RAW_PREFIX = "@@RAWFLOAT@@"


def _format_float(value: float) -> str:
    """Kürzeste, verlustfrei rücklesbare Darstellung eines Floats; große oder
    sehr kleine Beträge in wissenschaftlicher Notation."""
    value = float(value)  # numpy-Skalare in einen echten Python-float wandeln
    if value != 0 and (abs(value) >= SCI_UPPER or abs(value) < SCI_LOWER):
        return np.format_float_scientific(value, unique=True, trim="0")
    return repr(value)


def _wrap_floats(obj: Any) -> Any:
    """Ersetzt (rekursiv) alle endlichen Floats durch einen markierten String,
    dessen Anführungszeichen beim Schreiben wieder entfernt werden."""
    if isinstance(obj, float):
        if np.isfinite(obj):
            return _RAW_PREFIX + _format_float(obj)
        return obj  # nan/inf: json-Standardverhalten beibehalten
    if isinstance(obj, dict):
        return {k: _wrap_floats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_wrap_floats(v) for v in obj]
    return obj


def _dumps(data: Dict[str, Any]) -> str:
    text = json.dumps(_wrap_floats(data), indent=4, ensure_ascii=False)
    # Anführungszeichen (und Marker) um die Float-Tokens wieder entfernen
    return re.sub('"' + re.escape(_RAW_PREFIX) + r'([^"]*)"', r"\1", text)



def update_json_file(key: str, data_dict: Dict[str, Any], file_path: Path = destination) -> None:
    """Versucht eine JSON-Datei zu öffnen und fügt ihr ein Dictionary unter einem

    bestimmten Schlüssel hinzu. Falls die Datei nicht existiert oder leer ist,
    wird sie erstellt.

    :param file_path: Pfad zur JSON-Datei (str)
    :param key: Der Schlüssel, unter dem das Dict gespeichert wird (str)
    :param data_dict: Das hinzuzufügende Dictionary (dict)
    """
    # Standardmäßig starten wir mit einem leeren Dictionary
    current_data = {}

    # Prüfen, ob die Datei existiert und nicht leer ist
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                current_data = json.load(f)
                # Sicherstellen, dass das Root-Element ein Dictionary ist
                if not isinstance(current_data, dict):
                    raise ValueError(
                        "Das Root-Element der JSON-Datei ist kein Dictionary."
                    )
        except (json.JSONDecodeError, ValueError) as e:
            # Falls die Datei korrupt ist, wird hier abgefangen.
            # Je nach Anwendungsfall kann hier auch ein Fehler geworfen werden.
            print(
                f"Warnung: Datei konnte nicht gelesen werden ({e}). "
                "Sie wird überschrieben."
            )
            current_data = {}

    # Das neue Dictionary unter dem angegebenen Schlüssel einfügen/überschreiben
    current_data[key] = data_dict

    # Daten formatiert zurückschreiben
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(_dumps(current_data))