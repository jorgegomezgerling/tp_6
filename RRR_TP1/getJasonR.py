import json
import sys

class GestorTokens:
    """Clase Singleton para gestionar tokens y claves desde un archivo JSON."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorTokens, cls).__new__(cls)
            cls._cargar_tokens(cls._instancia)
        return cls._instancia

    @staticmethod
    def _cargar_tokens(self):
        """Cargar tokens desde el archivo JSON."""
        with open('sitedata.json') as archivo:
            self.tokens = json.load(archivo)

    def obtener_token(self, nombre):
        """Obtener la clave del token por nombre."""
        return self.tokens.get(nombre)

class CuentaBancaria:
    """Clase que representa una cuenta bancaria con un token y saldo."""
    def __init__(self, token, saldo):
        self.token = token
        self.saldo = saldo

    def retirar(self, cantidad):
        """Retirar una cantidad de la cuenta si hay fondos suficientes."""
        if self.saldo >= cantidad:
            self.saldo -= cantidad
            return True
        return False

    def depositar(self, cantidad):
        """Depositar una cantidad en la cuenta."""
        self.saldo += cantidad

    def obtener_saldo(self):
        """Obtener el saldo actual de la cuenta."""
        return self.saldo

class IteradorPagos:
    """Clase de iterador para iterar sobre pagos."""
    def __init__(self, pagos):
        self._pagos = pagos
        self._indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._indice < len(self._pagos):
            resultado = self._pagos[self._indice]
            self._indice += 1
            return resultado
        raise StopIteration

class ProcesadorPagos:
    """Clase para procesar pagos usando cuentas bancarias y mantener un registro de transacciones."""
    def __init__(self):
        self.cuentas = {
            "token1": CuentaBancaria("C598-ECF9-F0F7-881A", 1000),
            "token2": CuentaBancaria("C598-ECF9-F0F7-881B", 2000)
        }
        self.pagos = self._cargar_pagos()
        self.ultima_cuenta = None  # Inicializar como None para empezar con selección aleatoria de token
        self.indice_token_actual = 0  # Índice para rastrear el último token usado para el pago

    def procesar_pago(self, numero_pedido, monto):
        """Procesar un pago y enrutarlo a una cuenta con un saldo más cercano al monto del pago."""
        mejor_cuenta = None
        mejor_diferencia = float('inf')  # Inicializar como infinito para encontrar el saldo más cercano

        for token, cuenta in self.cuentas.items():
            if cuenta.saldo >= monto:
                diferencia = abs(cuenta.saldo - monto)
                if diferencia < mejor_diferencia:
                    mejor_cuenta = token
                    mejor_diferencia = diferencia

        if mejor_cuenta:
            cuenta = self.cuentas[mejor_cuenta]
            cuenta.retirar(monto)
            self.pagos.append((numero_pedido, mejor_cuenta, monto))
            self.ultima_cuenta = mejor_cuenta
            self._guardar_pagos()
            return mejor_cuenta, monto
        else:
            return None, 0

    def _cargar_pagos(self):
        """Cargar pagos desde un archivo JSON."""
        try:
            with open('payments.json') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []

    def _guardar_pagos(self):
        """Guardar pagos en un archivo JSON."""
        with open('payments.json', 'w') as archivo:
            json.dump(self.pagos, archivo)

    def listar_pagos(self):
        """Listar todos los pagos realizados en orden cronológico."""
        return IteradorPagos(self.pagos)

    def limpiar_pagos(self):
        """Borrar todos los pagos y restablecer saldos de cuentas a 0."""
        self.pagos = []
        for cuenta in self.cuentas.values():
            cuenta.saldo = 0

def main():
    if len(sys.argv) < 2:
        print("Uso: python getJasonR.py <sitedata.json> <monto> O python getJasonR.py listar O python getJasonR.py limpiar")
        return

    if sys.argv[1] == "listar":
        procesador = ProcesadorPagos()
        print("Lista de pagos:")
        for pago in procesador.listar_pagos():
            print(pago)
        return

    if sys.argv[1] == "limpiar":
        procesador = ProcesadorPagos()
        procesador.limpiar_pagos()
        print("Todos los pagos han sido eliminados.")
        return

    if len(sys.argv) != 3:
        print("Uso: python getJasonR.py <sitedata.json> <monto>")
        return

    archivo_sitedata = sys.argv[1]
    monto = int(sys.argv[2])

    # Procesar pago
    procesador = ProcesadorPagos()
    numero_pedido = len(procesador.pagos) + 1
    token_procesado, monto_procesado = procesador.procesar_pago(numero_pedido, monto)

    if token_procesado:
        print(f"Pago {numero_pedido} procesado: token={token_procesado}, monto={monto_procesado}")
    else:
        print(f"Pago {numero_pedido} fallido: fondos insuficientes")

    # Listar pagos
    print("Lista de pagos:")
    for pago in procesador.listar_pagos():
        print(pago)

if __name__ == "__main__":
    main()
