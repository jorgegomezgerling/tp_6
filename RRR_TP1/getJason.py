import json
import sys

# Verificar que se proporcionen los argumentos necesarios
if len(sys.argv) != 3:
    print("Uso: ./getJason.py {path archivo JSON}/{nombre archivo JSON}.json {clave}")
    sys.exit(1)

jsonfile = sys.argv[1]
jsonkey = sys.argv[2]

try:
    # Leer el archivo JSON
    with open(jsonfile, "r") as myfile:
        data = myfile.read()
    obj = json.loads(data)

    # Verificar si la clave existe en el archivo JSON
    if jsonkey in obj:
        print(f"{{1.0}}{obj[jsonkey]}")
    else:
        print(f"La clave '{jsonkey}' no fue encontrada en el archivo JSON.")
except FileNotFoundError:
    print(f"El archivo '{jsonfile}' no existe.")
except json.JSONDecodeError:
    print(f"El archivo '{jsonfile}' no es un archivo JSON válido.")
