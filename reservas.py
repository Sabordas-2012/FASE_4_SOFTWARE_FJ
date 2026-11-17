
# ============================================
# Proyecto: Sistema Integral de Gestion Software FJ
# Archivo: reservas.py
# Descripcion: Administracion de reservas
# ============================================

from excepciones import (
    ErrorValidacion,
    ErrorReserva,
    ReservaNoPermitida
)

from logs import RegistroSistema


# Clase Reserva
class Reserva:

    def __init__(self, identificador, cliente, servicio, duracion):

        if not identificador:
            raise ErrorValidacion("El ID de la reserva es obligatorio.")

        if cliente is None:
            raise ErrorValidacion("Debe seleccionar un cliente.")

        if servicio is None:
            raise ErrorValidacion("Debe seleccionar un servicio.")

        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ErrorValidacion("La duracion debe ser un entero positivo.")

        servicio.validar_disponibilidad()
        servicio.validar_parametros(duracion)

        self.__identificador = identificador
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__costo = 0

        RegistroSistema.registrar_evento(
            f"Reserva {identificador} creada correctamente."
        )

    @property
    def identificador(self):
        return self.__identificador

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    # Confirmar una reserva
    def confirmar(self):

        if self.__estado != "Pendiente":
            raise ReservaNoPermitida(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__servicio.validar_disponibilidad()

        self.__estado = "Confirmada"

        RegistroSistema.registrar_evento(
            f"Reserva {self.__identificador} confirmada."
        )

        return "Reserva confirmada correctamente."

    # Cancelar una reserva
    def cancelar(self):

        if self.__estado == "Cancelada":
            raise ReservaNoPermitida(
                "La reserva ya se encuentra cancelada."
            )

        if self.__estado == "Procesada":
            raise ReservaNoPermitida(
                "No se puede cancelar una reserva procesada."
            )

        self.__estado = "Cancelada"

        RegistroSistema.registrar_evento(
            f"Reserva {self.__identificador} cancelada."
        )

        return "Reserva cancelada correctamente."

    # Calcular costo con parametros opcionales
    def calcular_total(self, descuento=0, impuesto=0):

        try:
            self.__costo = self.__servicio.calcular_costo(
                self.__duracion,
                descuento,
                impuesto
            )

            return self.__costo

        except Exception as error:

            RegistroSistema.registrar_error(
                f"Error al calcular la reserva {self.__identificador}: {error}"
            )

            raise ErrorReserva(
                "No fue posible calcular el costo de la reserva."
            ) from error

    # Procesar la reserva
    def procesar(self, descuento=0, impuesto=0):

        try:

            if self.__estado != "Confirmada":
                raise ReservaNoPermitida(
                    "La reserva debe estar confirmada para procesarse."
                )

            self.__costo = self.calcular_total(
                descuento,
                impuesto
            )

            self.__estado = "Procesada"

            RegistroSistema.registrar_evento(
                f"Reserva {self.__identificador} procesada. "
                f"Total: ${self.__costo:,.2f}"
            )

            return self.__costo

        except (ErrorReserva, ReservaNoPermitida) as error:

            RegistroSistema.registrar_error(
                f"Error al procesar reserva {self.__identificador}: {error}"
            )

            raise

        finally:

            RegistroSistema.registrar_evento(
                f"Finalizacion del intento de procesamiento "
                f"de reserva {self.__identificador}."
            )

    # Mostrar informacion de la reserva
    def mostrar_info(self):

        return (
            f"\n--- INFORMACION DE LA RESERVA ---\n"
            f"ID: {self.__identificador}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duracion: {self.__duracion}\n"
            f"Estado: {self.__estado}\n"
            f"Costo: ${self.__costo:,.2f}"
        )


# Administrador de reservas
class GestorReservas:

    def __init__(self):

        self.__reservas = []

    # Crear y almacenar una reserva
    def crear_reserva(self, identificador, cliente, servicio, duracion):

        reserva = Reserva(
            identificador,
            cliente,
            servicio,
            duracion
        )

        self.__reservas.append(reserva)

        return reserva

    # Buscar una reserva por identificador
    def buscar_reserva(self, identificador):

        for reserva in self.__reservas:

            if reserva.identificador == identificador:
                return reserva

        raise ErrorReserva(
            f"No se encontro la reserva {identificador}."
        )

    # Listar todas las reservas
    def listar_reservas(self):

        return self.__reservas.copy()

    # Mostrar todas las reservas
    def mostrar_reservas(self):

        if not self.__reservas:
            return "No hay reservas registradas."

        return "\n".join(
            reserva.mostrar_info()
            for reserva in self.__reservas
        )


    # Cancelar una reserva por identificador
    def cancelar_reserva(self, identificador):

        reserva = self.buscar_reserva(identificador)

        return reserva.cancelar()


    # Confirmar una reserva por identificador
    def confirmar_reserva(self, identificador):

        reserva = self.buscar_reserva(identificador)

        return reserva.confirmar()
