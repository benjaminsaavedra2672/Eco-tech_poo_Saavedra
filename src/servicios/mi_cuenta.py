"""Operaciones personales: el ID se obtiene siempre de la sesión."""
from servicios.permisos import exigir_empleado
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

def mi_perfil(sesion):
    return EmpleadoDAO.buscar_por_id(exigir_empleado(sesion))

def actualizar_mis_datos(sesion, nombre, correo):
    empleado_id = exigir_empleado(sesion)
    empleado = EmpleadoDAO.buscar_por_id(empleado_id)
    if empleado is None:
        raise ValueError("No se encontró el perfil asociado a la sesión.")
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)
    return EmpleadoDAO.actualizar_nombre_correo(empleado_id, nombre, correo)

def mis_registros(sesion):
    from persistencia.registro_tiempo_dao import RegistroTiempoDAO
    return RegistroTiempoDAO.listar_por_empleado(exigir_empleado(sesion))
