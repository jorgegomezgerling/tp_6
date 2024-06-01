# getJason.py
# © UADERFCyT-IS2 2024, todos los derechos reservados.
# Este programa permite extraer la clave de acceso API para utilizar los servicios del Banco XXX.
# versión 1.1

import json
import sys

class TokenExtractor:
    _instance = None

    @staticmethod
    def get_instance():
        """Devuelve la instancia única de TokenExtractor (Singleton)."""
        if TokenExtractor._instance is None:
            TokenExtractor()
        return TokenExtractor._instance

    def __init__(self):
        """Constructor de la clase solo una instancia."""
        if TokenExtractor._instance is not None:
            raise Exception("Singleton")
        else:
            TokenExtractor._instance = self

    def extract_token(self, json_path, token_key="token1"):
        """Toma el token desde el archivo JSON dado."""
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
                if token_key in data:
                    return f"{{1.0}}{data[token_key]}"
                else:
                    return f"Error: El token key: '{token_key}' no se encuentra en el JSON File"
        except FileNotFoundError:
            return "Error: El archivo JSON no se encuentra."
        except json.JSONDecodeError:
            return "Error: Falla en decoficiar el JSON desde el archivo"
        except Exception as e:
            return f"Error inesperado: {str(e)}"

def main():
    """Función principal que maneja la lógica de línea de comandos."""
    if len(sys.argv) < 2:
        print("Uso: getJason.py <json_file_path> [<token_key>]")
        return

    json_path = sys.argv[1]
    token_key = sys.argv[2] if len(sys.argv) > 2 else "token1"

    if json_path == "-v":
        print("versión 1.1")
        return

    extractor = TokenExtractor.get_instance()
    result = extractor.extract_token(json_path, token_key)
    print(result)

if __name__ == "__main__":
    main()
