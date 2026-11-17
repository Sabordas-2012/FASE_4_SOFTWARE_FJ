
# ============================================
# Proyecto: Sistema Integral de Gestion Software FJ
# Archivo: servicios.py
# Descripcion: Gestion de servicios especializados
# ============================================

from abc import ABC, abstractmethod
import math

from excepciones import (
    ErrorValidacion,
    ServicioNoDisponible
)

from logs import RegistroSistema


# Clase abstracta Servicio
class Servicio(ABC):

    def __init__(self, identificador, nombre, precio_base):

        if not identificador:
            raise ErrorValidacion(
                "El ID del servicio es obligatorio."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise ErrorValidacion(
                "El nombre del servicio es obligatorio."
            )

        if (
            isinstance(precio_base, bool)
            or not isinstance(precio_base, (int, float))
            or not math.isfinite(precio_base)
            or precio_base <= 0
        ):
            raise ErrorValidacion(
                "El precio base debe ser un numero mayor que cero."
            )

        self._identificador = identificador
        self._nombre = nombre.strip()
        self._precio_base = precio_base
        self._disponible = True

    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise ErrorValidacion(
                "La disponibilidad debe ser True o False."
            )

        self._disponible = estado

        RegistroSistema.registrar_evento(
            f"Disponibilidad del servicio {self._nombre}: {estado}"
        )

    def validar_disponibilidad(self):

        if not self._disponible:
            raise ServicioNoDisponible(
                f"El servicio {self._nombre} no esta disponible."
            )

    @abstractmethod
    def calcular_costo(self, cantidad, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, cantidad):
        pass

    def __str__(self):
        return f"{self._nombre} - ${self._precio_base:,.2f}"

    # Metodo que simula la sobrecarga en Python
    def calcular_costo_sobrecargado(self, *args):

        if len(args) == 1:

            cantidad = args[0]

            return self.calcular_costo(cantidad)

        elif len(args) == 2:

            cantidad, descuento = args

            return self.calcular_costo(
                cantidad,
                descuento
            )

        elif len(args) == 3:

            cantidad, descuento, impuesto = args

            return self.calcular_costo(
                cantidad,
                descuento,
                impuesto
            )

        else:

            raise ErrorValidacion(
                "Debe ingresar uno, dos o tres parametros."
            )

    # Metodo flexible con parametros opcionales
    def calcular_costo_flexible(
        self,
        cantidad,
        descuento=0,
        impuesto=0
    ):

        return self.calcular_costo(
            cantidad,
            descuento,
            impuesto
        )


# Servicio especializado: Reserva de salas
class ServicioSala(Servicio):

    def __init__(self, identificador, nombre, precio_base, capacidad):

        super().__init__(identificador, nombre, precio_base)

        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad <= 0
        ):
            raise ErrorValidacion(
                "La capacidad debe ser un entero positivo."
            )

        self.__capacidad = capacidad

    def validar_parametros(self, cantidad):

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ErrorValidacion(
                "Las horas deben ser un entero positivo."
            )

    def calcular_costo(self, cantidad, descuento=0, impuesto=0):

        self.validar_parametros(cantidad)
        self.validar_disponibilidad()
        validar_porcentajes(descuento, impuesto)

        subtotal = self.precio_base * cantidad
        total = subtotal - (subtotal * descuento / 100)
        total += total * impuesto / 100

        return round(total, 2)

    def describir_servicio(self):

        return (
            f"Sala: {self.nombre}. "
            f"Capacidad: {self.__capacidad} personas. "
            f"Precio por hora: ${self.precio_base:,.2f}"
        )


# Servicio especializado: Alquiler de equipos
class ServicioEquipo(Servicio):

    def __init__(self, identificador, nombre, precio_base, tipo_equipo):

        super().__init__(identificador, nombre, precio_base)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ErrorValidacion(
                "Debe especificar el tipo de equipo."
            )

        self.__tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, cantidad):

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ErrorValidacion(
                "La cantidad de equipos debe ser positiva."
            )

    def calcular_costo(self, cantidad, descuento=0, impuesto=0):

        self.validar_parametros(cantidad)
        self.validar_disponibilidad()
        validar_porcentajes(descuento, impuesto)

        subtotal = self.precio_base * cantidad
        total = subtotal - (subtotal * descuento / 100)
        total += total * impuesto / 100

        return round(total, 2)

    def describir_servicio(self):

        return (
            f"Alquiler de equipo: {self.nombre}. "
            f"Tipo: {self.__tipo_equipo}. "
            f"Precio por unidad: ${self.precio_base:,.2f}"
        )


# Servicio especializado: Asesorias
class ServicioAsesoria(Servicio):

    def __init__(self, identificador, nombre, precio_base, especialidad):

        super().__init__(identificador, nombre, precio_base)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ErrorValidacion(
                "Debe especificar una especialidad."
            )

        self.__especialidad = especialidad.strip()

    def validar_parametros(self, cantidad):

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ErrorValidacion(
                "Las horas de asesoria deben ser positivas."
            )

    def calcular_costo(self, cantidad, descuento=0, impuesto=0):

        self.validar_parametros(cantidad)
        self.validar_disponibilidad()
        validar_porcentajes(descuento, impuesto)

        subtotal = self.precio_base * cantidad
        total = subtotal - (subtotal * descuento / 100)
        total += total * impuesto / 100

        return round(total, 2)

    def describir_servicio(self):

        return (
            f"Asesoria: {self.nombre}. "
            f"Especialidad: {self.__especialidad}. "
            f"Precio por hora: ${self.precio_base:,.2f}"
        )


# Validacion general de descuentos e impuestos
def validar_porcentajes(descuento, impuesto):

    if (
        isinstance(descuento, bool)
        or not isinstance(descuento, (int, float))
        or not math.isfinite(descuento)
    ):
        raise ErrorValidacion(
            "El descuento debe ser numerico y finito."
        )

    if (
        isinstance(impuesto, bool)
        or not isinstance(impuesto, (int, float))
        or not math.isfinite(impuesto)
    ):
        raise ErrorValidacion(
            "El impuesto debe ser numerico y finito."
        )

    if not 0 <= descuento <= 100:
        raise ErrorValidacion(
            "El descuento debe estar entre 0 y 100."
        )

    if not 0 <= impuesto <= 100:
        raise ErrorValidacion(
            "El impuesto debe estar entre 0 y 100."
        )


RegistroSistema.registrar_evento(
    "Modulo de servicios especializado cargado correctamente."
)
