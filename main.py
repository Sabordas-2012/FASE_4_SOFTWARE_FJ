
# ==================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Curso: Programacion
# Proyecto: Sistema Integral de Gestion Software FJ
# Fase 4
# Archivo: main.py
# ==================================================

from entidades import Cliente

from servicios import (
    ServicioSala,
    ServicioEquipo,
    ServicioAsesoria
)

from reservas import GestorReservas

from excepciones import (
    ErrorValidacion,
    ErrorCliente,
    ErrorReserva,
    ErrorServicio
)

from logs import RegistroSistema


def ejecutar_sistema():

    print("=" * 60)
    print("       SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("=" * 60)

    clientes = []
    servicios = []

    gestor = GestorReservas()

    # ==============================================
    # OPERACION 1: Registrar un cliente valido
    # ==============================================

    print("\nOPERACION 1: Registro de cliente")

    try:
        cliente1 = Cliente(
            "C001",
            "Laura Martinez",
            "12345678",
            "laura@gmail.com",
            "3101234567"
        )

        clientes.append(cliente1)

        print("Cliente registrado correctamente.")
        print(cliente1.mostrar_info())

    except (ErrorValidacion, ErrorCliente) as error:
        print(f"Error: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 2: Intentar registrar cliente invalido
    # ==============================================

    print("\nOPERACION 2: Registro de cliente invalido")

    try:
        cliente_invalido = Cliente(
            "C002",
            "Lu",
            "123",
            "correo_invalido",
            "123"
        )

        clientes.append(cliente_invalido)

    except (ErrorValidacion, ErrorCliente) as error:
        print(f"Error controlado: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 3: Crear servicio de sala
    # ==============================================

    print("\nOPERACION 3: Crear servicio de sala")

    try:
        sala = ServicioSala(
            "S001",
            "Sala de reuniones",
            50000,
            20
        )

        servicios.append(sala)

        print(sala.describir_servicio())

    except (ErrorValidacion, ErrorServicio) as error:
        print(f"Error: {error}")
        RegistroSistema.registrar_error(str(error))

   
    # ==============================================
    # PRUEBA: METODO CON VARIANTES DE SOBRECARGA
    # ==============================================

    print("\nPRUEBA: METODO CON VARIANTES DE SOBRECARGA")

    try:

        print(
            "Variante 1 - Solo cantidad:",
            sala.calcular_costo_sobrecargado(2)
        )

        print(
            "Variante 2 - Cantidad y descuento:",
            sala.calcular_costo_sobrecargado(2, 10)
        )

        print(
            "Variante 3 - Cantidad, descuento e impuesto:",
            sala.calcular_costo_sobrecargado(2, 10, 19)
        )

    except (ErrorValidacion, ErrorServicio) as error:

        print(f"Error en las variantes de calculo: {error}")
        RegistroSistema.registrar_error(str(error))


    # ==============================================
    # OPERACION 4: Crear servicio de equipos
    # ==============================================

    print("\nOPERACION 4: Crear servicio de equipos")

    try:
        equipo = ServicioEquipo(
            "S002",
            "Computador portatil",
            30000,
            "Equipo de computo"
        )

        servicios.append(equipo)

        print(equipo.describir_servicio())

    except (ErrorValidacion, ErrorServicio) as error:
        print(f"Error: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 5: Crear servicio de asesoria
    # ==============================================

    print("\nOPERACION 5: Crear servicio de asesoria")

    try:
        asesoria = ServicioAsesoria(
            "S003",
            "Asesoria en programacion",
            80000,
            "Desarrollo de software"
        )

        servicios.append(asesoria)

        print(asesoria.describir_servicio())

    except (ErrorValidacion, ErrorServicio) as error:
        print(f"Error: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 6: Servicio con precio incorrecto
    # ==============================================

    print("\nOPERACION 6: Servicio con precio incorrecto")

    try:
        servicio_invalido = ServicioSala(
            "S004",
            "Sala incorrecta",
            -5000,
            10
        )

        servicios.append(servicio_invalido)

    except (ErrorValidacion, ErrorServicio) as error:
        print(f"Error controlado: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 7: Crear una reserva
    # ==============================================

    print("\nOPERACION 7: Crear reserva")

    try:
        reserva1 = gestor.crear_reserva(
            "R001",
            cliente1,
            sala,
            3
        )

        print("Reserva creada correctamente.")
        print(reserva1.mostrar_info())

    except (ErrorValidacion, ErrorServicio, ErrorReserva) as error:
        print(f"Error al crear reserva: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 8: Confirmar y procesar reserva
    # ==============================================

    print("\nOPERACION 8: Confirmar y procesar reserva")

    try:
        print(gestor.confirmar_reserva("R001"))

        total = reserva1.procesar(
            descuento=10,
            impuesto=19
        )

        print("Reserva procesada correctamente.")
        print(f"Total a pagar: ${total:,.2f}")

    except ErrorReserva as error:
        print(f"Error: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 9: Crear y cancelar reserva
    # ==============================================

    print("\nOPERACION 9: Cancelar reserva")

    try:
        reserva2 = gestor.crear_reserva(
            "R002",
            cliente1,
            equipo,
            2
        )

        print(gestor.cancelar_reserva("R002"))

    except (ErrorReserva, ErrorValidacion, ErrorServicio) as error:
        print(f"Error: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 10: Servicio no disponible
    # ==============================================

    print("\nOPERACION 10: Servicio no disponible")

    try:
        asesoria.cambiar_disponibilidad(False)

        reserva3 = gestor.crear_reserva(
            "R003",
            cliente1,
            asesoria,
            2
        )

    except (ErrorServicio, ErrorValidacion, ErrorReserva) as error:
        print(f"Error controlado: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 11: Calculo con descuento incorrecto
    # ==============================================

    print("\nOPERACION 11: Calculo con descuento incorrecto")

    try:
        sala.calcular_costo(
            2,
            descuento=150,
            impuesto=19
        )

    except ErrorValidacion as error:
        print(f"Error controlado: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # OPERACION 12: Buscar reserva inexistente
    # ==============================================

    print("\nOPERACION 12: Buscar reserva inexistente")

    try:
        gestor.buscar_reserva("R999")

    except ErrorReserva as error:
        print(f"Error controlado: {error}")
        RegistroSistema.registrar_error(str(error))

    # ==============================================
    # RESUMEN FINAL DEL SISTEMA
    # ==============================================

    print("\n" + "=" * 60)
    print("             RESUMEN DEL SISTEMA")
    print("=" * 60)

    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios creados: {len(servicios)}")
    print(f"Reservas gestionadas: {len(gestor.listar_reservas())}")

    print("\nLISTADO DE RESERVAS:")

    print(gestor.mostrar_reservas())

    print("\nEl sistema finalizo correctamente.")
    print("Los eventos y errores fueron registrados en eventos.log.")

    RegistroSistema.registrar_evento(
        "Ejecucion del sistema finalizada correctamente."
    )


# ==============================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==============================================

if __name__ == "__main__":

    try:
        ejecutar_sistema()

    except Exception as error:
        print(f"Error inesperado en el sistema: {error}")

        RegistroSistema.registrar_error(
            f"Error general de ejecucion: {error}"
        )

    else:
        print("\nEjecucion sin errores generales.")

    finally:
        print("\nCierre del programa Software FJ.")
