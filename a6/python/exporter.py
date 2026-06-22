import json
import os
from pathlib import Path
from typing import Any, Dict

current_file = Path(__file__).resolve().parent
destination = current_file.parent / "plots" / "export.json"



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
        json.dump(current_data, f, indent=4, ensure_ascii=False)