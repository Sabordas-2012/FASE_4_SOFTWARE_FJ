
# ============================================
# Proyecto: Sistema Integral Software FJ
# Archivo: logs.py
# Descripción: Registro de eventos y errores
# ============================================

import logging

# Configuración del sistema de registro
logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class RegistroSistema:

    @staticmethod
    def registrar_evento(mensaje):
        """Registra los eventos importantes del sistema."""
        logging.info(mensaje)

    @staticmethod
    def registrar_error(mensaje):
        """Registra los errores que ocurren durante la ejecución."""
        logging.error(mensaje)

    @staticmethod
    def registrar_advertencia(mensaje):
        """Registra situaciones que requieren atención."""
        logging.warning(mensaje)
