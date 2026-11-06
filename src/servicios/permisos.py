"""Controles obligatorios de autorización, independientes de los menús."""

def exigir_sesion(sesion):
    if sesion is None or getattr(sesion, "id", None) is None:
        raise PermissionError("Debe iniciar sesión.")
    if getattr(sesion, "rol", None) not in ("admin", "empleado"):
        raise PermissionError("Rol de sesión no válido.")
    return sesion

def exigir_admin(sesion):
    exigir_sesion(sesion)
    if sesion.rol != "admin":
        raise PermissionError("Esta operación requiere permisos de administrador.")
    return sesion

def exigir_empleado(sesion):
    exigir_sesion(sesion)
    if not isinstance(getattr(sesion, "empleado_id", None), int) or sesion.empleado_id <= 0:
        raise PermissionError("La sesión no tiene empleado asociado.")
    return sesion.empleado_id
