
# ============================================
# Proyecto: Sistema Integral Software FJ
# Archivo: excepciones.py
# Descripción: Excepciones personalizadas
# ============================================

class ErrorSistema(Exception):
    """Excepción base para los errores del sistema."""
    pass


class ErrorValidacion(ErrorSistema):
    """Se presenta cuando los datos ingresados no son válidos."""
    pass


class ErrorCliente(ErrorSistema):
    """Se presenta cuando ocurre un error con un cliente."""
    pass


class ErrorServicio(ErrorSistema):
    """Se presenta cuando ocurre un error con un servicio."""
    pass


class ErrorReserva(ErrorSistema):
    """Se presenta cuando una reserva no puede realizarse."""
    pass


class ServicioNoDisponible(ErrorServicio):
    """Se presenta cuando un servicio no está disponible."""
    pass


class ReservaNoPermitida(ErrorReserva):
    """Se presenta cuando una operación de reserva no está permitida."""
    pass
