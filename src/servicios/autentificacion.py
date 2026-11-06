"""Autenticación y autorización centralizadas."""
from persistencia.usuario_dao import UsuarioDAO


def iniciar_sesion(username, password):
    try:
        usuario = UsuarioDAO.buscar_por_username(username)
    except (ValueError, TypeError):
        return None
    if usuario and usuario.autenticar(password):
        return usuario
    return None


def es_administrador(usuario):
    return bool(usuario and usuario.rol == "admin")


def exigir_administrador(usuario):
    if not es_administrador(usuario):
        raise PermissionError("Esta operación requiere permisos de administrador.")
