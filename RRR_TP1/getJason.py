import json
import sys
from datetime import datetime

"""“copyright UADER-
FCyT-IS2©2024 todos los derechos reservados)."""


class JSONTokenExtractor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JSONTokenExtractor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.version = "1.1"

    def extract_token(self, jsonfile, jsonkey):
        try:
            with open(jsonfile, "r") as myfile:
                data = myfile.read()
            obj = json.loads(data)

            if jsonkey in obj:
                return f"{{1.0}}{obj[jsonkey]}"
            else:
                return f"Error: La clave '{jsonkey}' no se encontró en el archivo JSON."
        except FileNotFoundError:
            return f"Error: No se encontró el archivo JSON especificado '{jsonfile}'."
        except json.JSONDecodeError:
            return f"Error: El archivo '{jsonfile}' no es un archivo JSON válido."

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "-v":
        print("Versión:", JSONTokenExtractor().version)
        sys.exit(0)
    elif len(sys.argv) != 3:
        print("Uso: python3.12 getJasonR.py {ruta al archivo JSON}/{nombre del archivo JSON}.json {clave}")
        sys.exit(1)

    jsonfile = sys.argv[1]
    jsonkey = sys.argv[2]

    extractor = JSONTokenExtractor()
    result = extractor.extract_token(jsonfile, jsonkey)
    print(result)

if __name__ == "__main__":
    main()
