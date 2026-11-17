
# ============================================
# Proyecto: Sistema Integral de Gestion Software FJ
# Archivo: entidades.py
# Descripcion: Clases abstractas y gestion de clientes
# ============================================

from abc import ABC, abstractmethod
import re

from excepciones import ErrorValidacion, ErrorCliente
from logs import RegistroSistema


# Clase abstracta general
class Entidad(ABC):

    def __init__(self, identificador):
        if not identificador:
            raise ErrorValidacion(
                "El identificador es obligatorio."
            )

        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_info(self):
        """Metodo abstracto para mostrar informacion."""
        pass


# Clase Cliente que hereda de Entidad
class Cliente(Entidad):

    def __init__(self, identificador, nombre, documento, correo, telefono):

        super().__init__(identificador)

        self.__nombre = self.validar_nombre(nombre)
        self.__documento = self.validar_documento(documento)
        self.__correo = self.validar_correo(correo)
        self.__telefono = self.validar_telefono(telefono)

        RegistroSistema.registrar_evento(
            f"Cliente registrado: {self.__nombre}"
        )

    # Validacion del nombre
    @staticmethod
    def validar_nombre(nombre):

        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ErrorCliente(
                "El nombre debe tener al menos 3 caracteres."
            )

        return nombre.strip()

    # Validacion del documento
    @staticmethod
    def validar_documento(documento):

        documento = str(documento).strip()

        if not documento.isdigit() or len(documento) < 5:
            raise ErrorCliente(
                "El documento debe contener minimo 5 digitos."
            )

        return documento

    # Validacion del correo electronico
    @staticmethod
    def validar_correo(correo):

        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"

        if not isinstance(correo, str) or not re.match(patron, correo):
            raise ErrorCliente(
                "El correo electronico no es valido."
            )

        return correo.lower().strip()

    # Validacion del telefono
    @staticmethod
    def validar_telefono(telefono):

        telefono = str(telefono).strip()

        if not telefono.isdigit() or len(telefono) < 7:
            raise ErrorCliente(
                "El telefono debe contener minimo 7 digitos."
            )

        return telefono

    # Propiedades para acceder a los atributos privados
    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # Metodo para mostrar informacion
    def mostrar_info(self):

        return (
            f"ID: {self.identificador}\n"
            f"Nombre: {self.__nombre}\n"
            f"Documento: {self.__documento}\n"
            f"Correo: {self.__correo}\n"
            f"Telefono: {self.__telefono}"
        )

    def __str__(self):
        return f"Cliente: {self.__nombre} - {self.__documento}"
